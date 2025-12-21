from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from PySide6.QtWidgets import QMessageBox

from Core.engine_inputs import EngineInputs  # adjust import path if needed


def _req_float(text: str, field: str) -> float:
    t = text.strip()
    if not t:
        raise ValueError(f"{field} is required.")
    try:
        return float(t)
    except ValueError as e:
        raise ValueError(f"{field} must be a number. Got: {text!r}") from e


class MainController:
    """
    Owns application state, reads inputs from the UI, runs analysis, and updates outputs.
    """

    def __init__(self, window):
        self.w = window
        self.last_inputs: Optional[EngineInputs] = None

        self._connect_signals()

    def _connect_signals(self) -> None:
        # Buttons (adapt names to yours)
        if hasattr(self.w, "run_btn"):
            self.w.run_btn.clicked.connect(self.run)

        if hasattr(self.w, "reset_btn"):
            self.w.reset_btn.clicked.connect(self.reset)

        # Menu actions (if you created them)
        if hasattr(self.w, "action_run"):
            self.w.action_run.triggered.connect(self.run)

        # Optional: auto-run or auto-update outputs when inputs change
        # self.w.noz_type.currentTextChanged.connect(lambda _: self.on_inputs_changed())

    # ------------------------
    # Build inputs from UI
    # ------------------------
    def build_inputs(self) -> EngineInputs:
        # Pc: you labeled in Bar in UI; store consistently (pick one)
        # If user enters Bar, convert to Pa:
        Pc_bar = _req_float(self.w.pc.text(), "Chamber pressure Pc (bar)")
        Pc_pa = Pc_bar * 1e5

        # Fuel / oxidizer (RocketCEA names)
        fuel = self.w.fuel.currentText().strip()
        ox = self.w.ox.currentText().strip()
        if not fuel:
            raise ValueError("Fuel is required.")
        if not ox:
            raise ValueError("Oxidizer is required.")

        # Ambient pressure: you show bar in UI
        if self.w.std_amb.isChecked():
            amb_pa = 101325.0
        else:
            amb_bar = _req_float(self.w.amb.text(), "Ambient pressure (bar)")
            amb_pa = amb_bar * 1e5

        # O/F: single or sweep
        if hasattr(self.w, "of_sweep") and self.w.of_sweep.isChecked():
            of_min = _req_float(self.w.of_min.text(), "O/F min")
            of_max = _req_float(self.w.of_max.text(), "O/F max")
            of_step = _req_float(self.w.of_inc.text(), "O/F step")

            if of_min <= 0 or of_max <= 0 or of_step <= 0:
                raise ValueError("O/F sweep values must be positive.")
            if of_min > of_max:
                raise ValueError("O/F min must be <= O/F max.")

            OF_min, OF_max, OF_increment = of_min, of_max, of_step
        else:
            of_single = _req_float(self.w.mr.text(), "O/F")
            if of_single <= 0:
                raise ValueError("O/F must be positive.")
            # Represent single point with min=max; increment can be 0 for your current dataclass
            OF_min, OF_max, OF_increment = of_single, of_single, 0.0

        # Nozzle
        thrust = _req_float(self.w.thrust.text(), "Thrust (N)")
        noz_type = self.w.noz_type.currentText().strip()

        # Conditional: bell percentage only used for Rao Bell
        bell_pct = ""
        if noz_type.lower() == "rao bell" and hasattr(self.w, "bell_pct"):
            bell_pct = self.w.bell_pct.currentText().strip()

        # Geometry/other fields (adapt to your widget names)
        conv = _req_float(self.w.convergence_angle.text(), "Convergence angle (deg)")
        div = _req_float(self.w.divergence_angle.text(), "Divergence angle (deg)")
        cr = _req_float(self.w.contraction_ratio.text(), "Contraction ratio")
        tr = _req_float(self.w.throat_ratio.text(), "Throat ratio")
        lstar = _req_float(self.w.lstar.text(), "L* (m)")

        return EngineInputs(
            chamber_pressure=Pc_pa,
            OF_min=OF_min,
            OF_max=OF_max,
            OF_increment=OF_increment,
            ambient_pressure=amb_pa,
            thrust=thrust,  # if you have it later
            convergent_angle=conv,
            divergent_angle=div,
            contraction_ratio=cr,
            throat_ratio=tr,
            l_star=lstar,
            bell_percentage=bell_pct,   # if your dataclass expects str
            fuel_name=fuel,
            oxidizer_name=ox,
            source="GUI",
        )
    
    def run(self) -> None:
            try:
                inputs = self.build_inputs()
            except ValueError as e:
                QMessageBox.warning(self.w, "Invalid inputs", str(e))
                return

            self.last_inputs = inputs

            # Call backend (replace with your actual pipeline)
            # results = Core.nozzle_pipeline.run(inputs) ...
            results = self._mock_results(inputs)

            self.update_outputs(results)

            if hasattr(self.w, "statusBar"):
                self.w.statusBar().showMessage("Analysis complete.")

    def reset(self) -> None:
        # Minimal reset: clear outputs; do not necessarily wipe all inputs
        if hasattr(self.w, "results_table"):
            for r in range(self.w.results_table.rowCount()):
                item = self.w.results_table.item(r, 1)
                if item:
                    item.setText("—")

        if hasattr(self.w, "report_view"):
            self.w.report_view.clear()

        if hasattr(self.w, "statusBar"):
            self.w.statusBar().showMessage("Reset complete.")
