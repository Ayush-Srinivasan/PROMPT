# GUI/controller.py
from __future__ import annotations
import numpy as np
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox

from Core.engine_inputs import EngineInputs
from Core.engine_analysis import engine_design_run
from Core.plots import plot_isp_vs_of, plot_temp_vs_of, plot_velocity_vs_of
from Isentropic.bell_nozzle_geometry import bell_nozzle_graph
from Isentropic.conical_nozzle_geometry import conical_nozzle_graph
from Core.plots import plot_nozzle_geometry, plot_nozzle_revolution

BAR_TO_PA = 1e5 # unit conversion from bar to pascals

class MainController:
    def __init__(self, view):
        self.view = view
        self.view.of_combo.currentIndexChanged.connect(self.on_of_combo_changed)

        # Your ui.py will emit these if you added the signals approach
        if hasattr(view, "run_requested"):
            view.run_requested.connect(self.on_run)
        if hasattr(view, "reset_requested"):
            view.reset_requested.connect(self.on_reset)

        # If you did NOT add signals and still want controller ownership,
        # you can also directly override by rebinding:
        # view.on_run = self.on_run
        # view.on_reset = self.on_reset

    def on_reset(self):
        v = self.view
        v._do_reset_ui()

        # also clear outputs table
        for r in range(v.results_table.rowCount()):
            v.results_table.setItem(r, 1, QTableWidgetItem("—"))
            
        self.view.reset_of_combo()
        self._last_results = None
        self._last_inputs = None

    def on_run(self):
        v = self.view

        try:
            eng_in = self._read_engine_inputs()
            self._last_inputs = eng_in
        except ValueError as e:
            QMessageBox.warning(v, "Input error", str(e))
            v.statusBar().showMessage("Input error")
            return

        v.console.append("Running analysis...")
        v.statusBar().showMessage("Running analysis...")

        try:
            results = engine_design_run(eng_in)
        except Exception as e:
            QMessageBox.critical(v, "Run failed", repr(e))
            v.console.append(f"Run failed: {repr(e)}")
            v.statusBar().showMessage("Run failed")
            return

        # Cache results ONLY after they exist
        self._last_results = results

        self._write_results(results)
        self._populate_of_combo(results)
        v.console.append("Complete.")
        v.statusBar().showMessage("Complete")

        
    def on_theme_changed(self):
        if getattr(self, "_last_results", None) is None:
            return
        self._write_results(self._last_results)
    # -----------------------
    # Build EngineInputs
    # -----------------------
    def _read_engine_inputs(self) -> EngineInputs:
        v = self.view

        # UI label says bar; EngineInputs wants Pa
        pc_bar = self._float_required(v.pc.text(), "Chamber Pressure (bar)")
        chamber_pressure_pa = pc_bar * BAR_TO_PA

        thrust_n = self._float_required(v.thrust.text(), "Thrust (N)")

        # Ambient pressure: your checkbox means "use standard 1.01325 bar"
        external_pressure_flag = v.std_amb.isChecked()
        if external_pressure_flag:
            amb_pa = 1.01325 * BAR_TO_PA
        else:
            amb_bar = self._float_required(v.amb.text(), "Ambient Pressure (bar)")
            amb_pa = amb_bar * BAR_TO_PA

        frozen_flag = v.frozen.isChecked()

        # O/F single or sweep
        sweep = v.of_sweep.isChecked()
        if sweep:
            of_val = None
            of_min = self._float_required(v.of_min.text(), "O/F min")
            of_max = self._float_required(v.of_max.text(), "O/F max")
            of_inc = self._float_required(v.of_inc.text(), "O/F step")
        else:
            of_val = self._float_required(v.mr.text(), "O/F")
            of_min = of_max = of_inc = None

        convergent_angle = self._float_required(v.convergence_angle.text(), "Convergence angle (deg)")
        divergent_angle = self._float_required(v.divergence_angle.text(), "Divergence angle (deg)")

        contraction_ratio = self._float_required(v.cr.text(), "Contraction ratio (Ac/At)")
        throat_ratio = self._float_required(v.throat_ratio.text(), "Throat ratio")
        l_star = self._float_required(v.lstar.text(), "L* (m)")

        fuel_name = v.fuel.currentText()
        oxidizer_name = v.ox.currentText()

        # Nozzle type affects whether bell percent matters
        noz_text = v.noz_type.currentText().strip().lower()

        if "bell" in noz_text:
            nozzle_type = "bell"
            bell_percent = int(v.bell_pct.currentText().split()[0])
        else:
            nozzle_type = "conical"
            bell_percent = None

        return EngineInputs(
            chamber_pressure=chamber_pressure_pa,

            # Single value run
            OF=of_val,

            # Sweep fields
            OF_min=of_min,
            OF_max=of_max,
            OF_increment=of_inc,

            external_pressure_flag=external_pressure_flag,
            ambient_pressure=amb_pa,

            frozen_flag=frozen_flag,

            thrust=thrust_n,
            nozzle_type=nozzle_type,
            convergent_angle=convergent_angle,
            divergent_angle=divergent_angle,
            contraction_ratio=contraction_ratio,
            throat_ratio=throat_ratio,
            l_star=l_star,

            bell_percent=bell_percent,
            fuel_name=fuel_name,
            oxidizer_name=oxidizer_name,
            source="GUI",
        )

    def _populate_of_combo(self, results):
        self.view.of_combo.blockSignals(True)
        self.view.of_combo.clear()

        of_values = results.cea.OF_Ratio

        for i, of in enumerate(of_values):
            self.view.of_combo.addItem(f"O/F = {of:.3f}", i)

        self.view.of_combo.setCurrentIndex(0)
        self.view.of_combo.setEnabled(len(of_values) > 1)
        self.view.of_combo.blockSignals(False)

    def on_of_combo_changed(self, _):
        if getattr(self, "_last_results", None) is None:
            return

        idx = self.view.of_combo.currentData()
        if idx is None:
            return
        self._update_visualizations(idx)

    # -----------------------
    # Write outputs
    # -----------------------

    def _write_results(self, results):
        v = self.view
        if not hasattr(v, "results_table"):
            return

        # O/F array (adjust field name if yours differs)
        OF = np.asarray(results.cea.OF_Ratio)

        perf = results.perf
        Isp = np.asarray(perf.Isp)
        cstar = np.asarray(perf.c_star)
        vexit = np.asarray(perf.v_exit)
        mdot = np.asarray(perf.mdot)

        Tc = np.asarray(results.cea.T_chamber)   # chamber temperature from CEAOutputs
        Tt = np.asarray(perf.T_throat)           # throat temperature from isentropic/analysis
        Te = np.asarray(perf.T_exit)             # exit temperature from isentropic/analysis

        n = OF.size
        v.results_table.setRowCount(n)

        for i in range(n):
            row = [
                f"{float(OF[i]):.3f}",
                f"{float(Isp[i]):.2f}",
                f"{float(cstar[i]):.1f}",
                f"{float(vexit[i]):.1f}",
                f"{float(mdot[i]):.6f}",
                f"{float(Tc[i]):.1f}",
                f"{float(Tt[i]):.1f}",
                f"{float(Te[i]):.1f}",
            ]
            for j, txt in enumerate(row):
                v.results_table.setItem(i, j, QTableWidgetItem(txt))

        theme = self.view.theme_mode()  # expects "system" | "light" | "dark" | "barbie"

        fig_isp = plot_isp_vs_of(OF, Isp, theme=theme)
        fig_vel = plot_velocity_vs_of(OF, vexit, cstar, theme=theme)
        fig_tmp = plot_temp_vs_of(OF, Tc, Tt, Te, theme=theme)

        self.view.set_plot_figures({
            "Isp vs O/F": fig_isp,
            "Velocity vs O/F": fig_vel,
            "T vs O/F": fig_tmp,
        })
        self._update_visualizations(idx=0)
    
    def _update_visualizations(self, idx: int):
        results = self._last_results
        inputs = self._last_inputs
        v = self.view

        if results.nozzle.__class__.__name__.lower().startswith("bell"):
            y, x = bell_nozzle_graph(results, inputs, idx=idx)
        else:
            xx, yy = conical_nozzle_graph(results, idx=idx)
            x, y = xx, yy
        theme = v.theme_mode()
        fig2d = plot_nozzle_geometry(x, y, theme=theme)
        fig3d = plot_nozzle_revolution(x, y, theme=theme, n_theta=80)

        v.set_viz_figures(fig2d, fig3d)

    # -----------------------
    # parsing helpers
    # -----------------------
    def _float_required(self, s: str, name: str) -> float:
        s = (s or "").strip()
        if not s:
            raise ValueError(f"{name} is required.")
        try:
            return float(s)
        except ValueError:
            raise ValueError(f"{name} must be numeric (got '{s}').")
