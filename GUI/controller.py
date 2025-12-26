# GUI/controller.py
from __future__ import annotations

from PySide6.QtWidgets import QTableWidgetItem, QMessageBox

from Core.engine_inputs import EngineInputs
from Core.engine_analysis import engine_design_run

BAR_TO_PA = 1e5 # unit conversion from bar to pascals

class MainController:
    def __init__(self, view):
        self.view = view

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

    def on_run(self):
        v = self.view

        try:
            eng_in = self._read_engine_inputs()
        except ValueError as e:
            QMessageBox.warning(v, "Input error", str(e))
            v.statusBar().showMessage("Input error")
            return

        v.console.append("Running analysis...")
        v.statusBar().showMessage("Running analysis...")

        try:
            results = engine_design_run(eng_in)  # must return something we can display
        except Exception as e:
            QMessageBox.critical(v, "Run failed", repr(e))
            v.console.append(f"Run failed: {repr(e)}")
            v.statusBar().showMessage("Run failed")
            return

        self._write_results(results)
        v.console.append("Complete.")
        v.statusBar().showMessage("Complete")

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
            bell_percent = v.bell_pct.currentText()
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

    # -----------------------
    # Write outputs
    # -----------------------
    def _write_results(self, results):
        v = self.view
        perf = results.perf

        import numpy as np
        idx = int(np.argmax(perf.Isp))  # choose the best-performing point

        def set_row(row_idx: int, value: str):
            v.results_table.setItem(row_idx, 1, QTableWidgetItem(value))

        # ui.py rows: ["Isp (vac)", "Isp (sea)", "c*", "At", "Ae", "mdot"]
        set_row(0, f"{float(perf.Isp[idx]):.2f} s")

        # You are not currently computing sea-level Isp separately; keep as placeholder or reuse
        set_row(1, "—")

        set_row(2, f"{float(perf.c_star[idx]):.1f} m/s")
        set_row(3, f"{float(perf.a_throat[idx]):.6e} m²")
        set_row(4, f"{float(perf.a_exit[idx]):.6e} m²")
        set_row(5, f"{float(perf.mdot[idx]):.6f} kg/s")


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
