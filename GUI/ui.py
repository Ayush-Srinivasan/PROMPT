# GUI/ui.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QDockWidget, QTabWidget, QApplication,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLineEdit, QComboBox, QPushButton, QLabel, QToolBar, QMessageBox, QCheckBox, 
)
from PySide6.QtGui import QAction, QDoubleValidator, QActionGroup, QGuiApplication
from PySide6.QtCore import Qt, Signal, QSettings, QSignalBlocker
from .themes import apply_theme
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from Data import Fuels, Oxidizers
from .widgets import make_searchable


class MainWindow(QMainWindow):

    # run and reset 
    run_requested = Signal()
    reset_requested = Signal()

    # exports
    export_cea_requested = Signal()
    export_engine_requested = Signal()
    export_nozzle_requested = Signal()

    def __init__(self):
        super().__init__()
        self.settings = QSettings("PROMPT", "RocketEngineDesignTool")
        self._theme_mode = self.settings.value("theme/mode", "system")

        self.setWindowTitle("PROMPT - Rocket Engine Design Tool")
        self._build_menu()
        self._build_top_command_area()
        self._build_docks()
        self._build_center()
        self._apply_validators()
        self.statusBar().showMessage("Ready")


    # --- (everything else stays the same as before) ---
    # Keep all _build_* methods and callbacks here

    def _build_menu(self):
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self._action("Open", self._noop))
        file_menu.addAction(self._action("Save", self._noop))
        file_menu.addSeparator()
        file_menu.addAction(self._action("Exit", self.close))

        view_menu = self.menuBar().addMenu("View")
        self.action_toggle_left = self._action("Toggle Feature Tree", self._toggle_left)
        self.action_toggle_right = self._action("Toggle Properties", self._toggle_right)
        self.action_toggle_bottom = self._action("Toggle Console", self._toggle_bottom)
        view_menu.addActions([self.action_toggle_left, self.action_toggle_right, self.action_toggle_bottom])

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self._action("About", self._about))

        settings_menu = self.menuBar().addMenu("Settings")

        self.theme_group = QActionGroup(self)
        self.theme_group.setExclusive(True)

        self.action_theme_system = QAction("Theme: System (Windows)", self, checkable=True)
        self.action_theme_light  = QAction("Theme: Light", self, checkable=True)
        self.action_theme_dark   = QAction("Theme: Dark", self, checkable=True)
        self.action_theme_barbie = QAction("Theme: Barbie", self, checkable=True)

        for a in (
            self.action_theme_system,
            self.action_theme_light,
            self.action_theme_dark,
            self.action_theme_barbie,
        ):
            self.theme_group.addAction(a)
            settings_menu.addAction(a)

        # Map actions → theme string
        self._theme_action_map = {
            self.action_theme_system: "system",
            self.action_theme_light:  "light",
            self.action_theme_dark:   "dark",
            self.action_theme_barbie: "barbie",
        }

        # ONE handler for all theme changes
        self.theme_group.triggered.connect(self._on_theme_action_selected)

        # Restore saved theme WITHOUT triggering handler
        mode = (self._theme_mode or "system").strip().lower()
        with QSignalBlocker(self.theme_group):
            if mode == "dark":
                self.action_theme_dark.setChecked(True)
            elif mode == "light":
                self.action_theme_light.setChecked(True)
            elif mode == "barbie":
                self.action_theme_barbie.setChecked(True)
            else:
                self.action_theme_system.setChecked(True)

        # Apply once
        self._apply_theme_mode(mode)

    def _on_theme_action_selected(self, action: QAction):
        mode = self._theme_action_map.get(action, "system")
        self._apply_theme_mode(mode)
        
    def _action(self, text, slot):
        act = QAction(text, self)
        act.triggered.connect(slot)
        return act

    # ----- Top "CommandManager" style area -----
    def _build_top_command_area(self):
        # This is an emulation: a tab bar that swaps which toolbar is visible.
        self.command_tabs = QTabWidget()
        self.command_tabs.setTabPosition(QTabWidget.North)
        self.command_tabs.setDocumentMode(True)  # more "app-like"
        self.command_tabs.setMovable(False)

        # Create toolbars for each tab
        self.tb_inputs = self._make_toolbar("Inputs", [
            ("Run", self.on_run),
            ("Reset", self.on_reset),
        ])
        self.tb_nozzle = self._make_toolbar("Nozzle", [
            ("Generate", self._noop),
            ("Preview", self._noop),
        ])
        self.tb_export = self._make_toolbar("Export", [
            ("Export CEA", self.export_cea_requested.emit),
            ("Export Engine Data", self.export_engine_requested.emit),
            ("Export CAD Datapoints", self.export_nozzle_requested.emit),
        ])

        # Add tabs (each tab content is a small placeholder widget)
        self.command_tabs.addTab(QWidget(), "Inputs")
        self.command_tabs.addTab(QWidget(), "Nozzle")
        self.command_tabs.addTab(QWidget(), "Export")

        self.command_tabs.currentChanged.connect(self._on_command_tab_changed)

        # Put the tab widget into a non-dock area at top by placing it in a toolbar container
        self.commandbar = QToolBar("Command Tabs")
        self.commandbar.setMovable(False)
        self.commandbar.setFloatable(False)
        self.commandbar.addWidget(self.command_tabs)
        self.addToolBar(Qt.TopToolBarArea, self.commandbar)

        # Show the first toolbar by default
        self.addToolBar(Qt.TopToolBarArea, self.tb_inputs)
        self._active_toolbar = self.tb_inputs

    def _make_toolbar(self, name, actions):
        tb = QToolBar(name)
        tb.setMovable(False)
        tb.setFloatable(False)
        for label, slot in actions:
            tb.addAction(self._action(label, slot))
        return tb

    def _on_command_tab_changed(self, idx: int):
        # swap toolbars based on tab selection
        mapping = {
            0: self.tb_inputs,
            1: self.tb_nozzle,
            2: self.tb_export,
        }
        new_tb = mapping.get(idx, self.tb_inputs)
        if new_tb is self._active_toolbar:
            return
        self.removeToolBar(self._active_toolbar)
        self.addToolBar(Qt.TopToolBarArea, new_tb)
        self._active_toolbar = new_tb

    # ----- Dock panels -----
    def _build_docks(self):
        # Left: Feature tree / project tree
        self.left_dock = QDockWidget("FeatureManager / Project", self)
        self.left_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.feature_tree = QTreeWidget()
        self.feature_tree.setHeaderHidden(True)

        root = QTreeWidgetItem(["Engine Project"])
        QTreeWidgetItem(root, ["Inputs"])
        QTreeWidgetItem(root, ["CEA / Performance"])
        QTreeWidgetItem(root, ["Nozzle Geometry"])
        QTreeWidgetItem(root, ["Exports"])
        self.feature_tree.addTopLevelItem(root)
        root.setExpanded(True)

        self.left_dock.setWidget(self.feature_tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)

        # Right: Properties manager (parameter entry)
        self.right_dock = QDockWidget("PropertyManager", self)
        self.right_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.right_dock.setWidget(self._build_properties_panel())
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)

        # Bottom: Console/log
        self.bottom_dock = QDockWidget("Console", self)
        self.bottom_dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("Log output will appear here...")
        self.bottom_dock.setWidget(self.console)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock)

    def _build_properties_panel(self) -> QWidget:
        # SolidWorks-like: groups of parameters
        panel = QWidget()
        layout = QVBoxLayout(panel)

        chamber = QGroupBox("Chamber / Propellants")
        f1 = QFormLayout(chamber)
        self.pc = QLineEdit()
        self.pc.setPlaceholderText("Pa (e.g., 20e5)")
        self.mr = QLineEdit()
        self.mr.setPlaceholderText("O/F (e.g., 2.5)")
        self.fuel = QComboBox()
        self.fuel.addItems(Fuels)
        make_searchable(self.fuel)
        self.ox = QComboBox()
        self.ox.addItems(Oxidizers)
        make_searchable(self.ox)


        # OF Ratio Sweep vs Single Value
        self.of_sweep = QCheckBox("Sweep O/F")
        self.of_min = QLineEdit()
        self.of_min.setPlaceholderText("O/F min (e.g., 2.0)")
        self.of_max = QLineEdit()
        self.of_max.setPlaceholderText("O/F max (e.g., 3.0)")
        self.of_inc = QLineEdit()
        self.of_inc.setPlaceholderText("O/F step (e.g., 0.1)")

        # default: single-value mode
        self.of_sweep.setChecked(False)
        self.of_min.setEnabled(False)
        self.of_max.setEnabled(False)
        self.of_inc.setEnabled(False)
        self.of_sweep.toggled.connect(self._on_of_sweep_toggled)        
        
        # Frozen or Equilibrium Check
        self.frozen = QCheckBox("Frozen Flow")


        # chamber pressure
        f1.addRow("Chamber Pressure (Bar):", self.pc)

        # fuel and ox choice
        f1.addRow("Fuel:", self.fuel)
        f1.addRow("Oxidizer:", self.ox)

        f1.addRow("O/F:", self.mr)
        f1.addRow(self.of_sweep)
        f1.addRow("O/F min:", self.of_min)
        f1.addRow("O/F max:", self.of_max)
        f1.addRow("O/F step:", self.of_inc)
        f1.addRow(self.frozen)





        nozzle = QGroupBox("Nozzle")
        f2 = QFormLayout(nozzle)
        self.thrust = QLineEdit()
        self.thrust.setPlaceholderText("4500 N")
        self.noz_type = QComboBox()
        self.noz_type.addItems(["Conical", "Rao Bell"])

        self.bell_pct = QComboBox()
        self.bell_pct.addItems(["60 Percent", "70 Percent", "80 Percent", "90 Percent", "100 Percent"])

        # ambient pressure 
        self.std_amb = QCheckBox("Use standard external pressure (1.01325 Bar)")
        self.amb = QLineEdit()
        self.amb.setPlaceholderText("Ambient pressure (Bar)")

        # defaults
        self.std_amb.setChecked(True)
        self.amb.setText("1.01325")
        self.amb.setEnabled(False)
        self.std_amb.toggled.connect(self._on_std_ambient_toggled)

        # convergence angle
        self.convergence_angle = QLineEdit()
        self.convergence_angle.setPlaceholderText("45")

        # divergence angle
        self.divergence_angle = QLineEdit()
        self.divergence_angle.setPlaceholderText("15")
        
        # contraction ratio
        self.cr = QLineEdit()
        self.cr.setPlaceholderText("4")

        # throat ratio
        self.throat_ratio = QLineEdit()
        self.throat_ratio.setPlaceholderText("0.05")

        # l_star
        self.lstar = QLineEdit()
        self.lstar.setPlaceholderText("0.8")

        # add rows 
        
        # Thrust
        f2.addRow("Thrust (N):", self.thrust)
        # Nozzle Type
        f2.addRow("Type:", self.noz_type)

        # bell percentage
        bell_label = QLabel("Bell %:")
        f2.addRow(bell_label, self.bell_pct)
        # store so we can hide/show later
        self._bell_label = bell_label
        self.noz_type.currentTextChanged.connect(self._on_nozzle_type_changed)
        self._on_nozzle_type_changed(self.noz_type.currentText())  # initialize state


        # ambient pressure
        f2.addRow(self.std_amb)
        f2.addRow("Ambient:", self.amb)

        # nozzle paramters
        f2.addRow("Convergence Angle (degrees):", self.convergence_angle)
        f2.addRow("Divergence Angle (degrees):", self.divergence_angle)
        f2.addRow("Contraction Ratio:", self.cr)
        f2.addRow("Throat Ratio:", self.throat_ratio)
        f2.addRow("L* (meters):", self.lstar)


        layout.addWidget(chamber)
        layout.addWidget(nozzle)
        layout.addStretch(1)
        return panel
    

    def _on_std_ambient_toggled(self, checked: bool):
        if checked:
            self.amb.setText("1.01325")
            self.amb.setEnabled(False)
        else:
            self.amb.setEnabled(True)   

    def _on_of_sweep_toggled(self, checked: bool):
        # checked = sweep mode
        self.mr.setEnabled(not checked)
        self.of_min.setEnabled(checked)
        self.of_max.setEnabled(checked)
        self.of_inc.setEnabled(checked)

        # Optional: quality-of-life defaults
        if checked:
            self.of_min.clear()
            self.of_max.clear()
            self.of_inc.clear()
            self.mr.clear()
        else:
            # leaving sweep mode; keep mr as-is or seed from min/max midpoint
            pass

    def _on_nozzle_type_changed(self, text: str):
        is_bell = (text.strip().lower() == "rao bell")
        # Show/hide both the label and the combo
        self._bell_label.setVisible(is_bell)
        self.bell_pct.setVisible(is_bell)

    def _build_workspace_tabs(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.setDocumentMode(True)  # looks more "app-like"

        # Results
        results = QWidget()
        results_layout = QVBoxLayout(results)

        self.results_table = QTableWidget(0, 8)
        self.results_table.setHorizontalHeaderLabels([
            "O/F", "Isp (s)", "c* (m/s)", "Exit Velocity (m/s)", "mdot (kg/s)",
            "Chamber Temp (K)", "Throat Temp (K)", "Exit Temp (K)"
            ])
        
        results_layout.addWidget(self.results_table)
        tabs.addTab(results, "Results")

        # Tab 2: Plots
        plots = QWidget()
        plots_layout = QVBoxLayout(plots)

        top_row = QHBoxLayout()
        self.metric_combo = QComboBox()
        self.metric_combo.addItems(["Isp vs O/F", "Velocity vs O/F", "T vs O/F"])
        self.metric_combo.currentIndexChanged.connect(self._render_selected_plot)
        top_row.addWidget(QLabel("Metric:"))
        top_row.addWidget(self.metric_combo)
        top_row.addStretch(1)

        plots_layout.addLayout(top_row)
        self.plot_widget = QWidget()
        self.plot_widget_layout = QVBoxLayout(self.plot_widget)

        # Keep references to avoid GC
        self._plot_toolbar = None
        self._plot_canvas = None

        plots_layout.addWidget(self.plot_widget, 1)

        tabs.addTab(plots, "Plots")

        # Visualization
        viz = QWidget()
        viz_layout = QVBoxLayout(viz)

        # top 
        self.of_combo = QComboBox()
        self.of_combo.setEnabled(False)
        self.of_label = QLabel("Visualization O/F:")
        of_row = QHBoxLayout()
        of_row.addWidget(self.of_label)
        of_row.addWidget(self.of_combo)
        of_row.addStretch(1)

        viz_layout.addLayout(of_row)

        # --- plots row (horizontal) ---
        plots_row = QHBoxLayout()

        # 2D plot
        self.viz2d_widget = QWidget()
        self.viz2d_layout = QVBoxLayout(self.viz2d_widget)
        plots_row.addWidget(self.viz2d_widget, 1)

        # 3D plot
        self.viz3d_widget = QWidget()
        self.viz3d_layout = QVBoxLayout(self.viz3d_widget)
        plots_row.addWidget(self.viz3d_widget, 1)

        # add plots row to main vertical layout
        viz_layout.addLayout(plots_row, 1)


        tabs.addTab(viz, "Visualization")


        # Drawing
        drawing = QLabel("Dimensioned drawing output will appear here.")
        drawing.setAlignment(Qt.AlignCenter)
        tabs.addTab(drawing, "Drawing")



        return tabs
    # ----- Center workspace -----
    def _build_center(self):
        # Center can be a placeholder "graphics/results" area for now.
        center = QWidget()
        layout = QVBoxLayout(center)

        header = QLabel("Workspace")
        header.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.workspace_tabs = self._build_workspace_tabs()
        layout.addWidget(self.workspace_tabs)

        self.setCentralWidget(center)

    # ----- Callbacks -----
    def on_run(self):
        self.console.append("Run pressed.")
        self.statusBar().showMessage("Running analysis...")
        self.run_requested.emit()

    def _do_reset_ui(self):
        # --- move ALL your field-clearing logic here ---
        # O/F sweep fields
        if hasattr(self, "pc"):
            self.pc.clear()
        if hasattr(self, "mr"):
            self.mr.clear()
        if hasattr(self, "of_min"):
            self.of_min.clear()
        if hasattr(self, "of_max"):
            self.of_max.clear()
        if hasattr(self, "of_inc"):
            self.of_inc.clear()
        if hasattr(self, "of_sweep"):
            self.of_sweep.setChecked(False)

        if hasattr(self, "thrust"):
            self.thrust.clear()

        self.noz_type.setCurrentIndex(0)
        if hasattr(self, "bell_pct"):
            self.bell_pct.setCurrentIndex(0)

        if hasattr(self, "std_amb"):
            self.std_amb.setChecked(True)
        if hasattr(self, "amb"):
            self.amb.setText("1.01325")

        for name in ["convergence_angle", "divergence_angle", "cr", "throat_ratio", "lstar"]:
            if hasattr(self, name):
                getattr(self, name).clear()

        self.console.append("Reset inputs.")
        self.statusBar().showMessage("Reset")

    def reset_of_combo(self):
        self.of_combo.blockSignals(True)
        self.of_combo.clear()
        self.of_combo.setEnabled(False)
        self.of_combo.blockSignals(False)

    def on_reset(self):
       self.reset_requested.emit()

    def _apply_validators(self):
        def dv(lo, hi, dec=6):
            v = QDoubleValidator(lo, hi, dec, self)
            v.setNotation(QDoubleValidator.StandardNotation)
            return v

        # Chamber / propellants
        # Pc is labeled bar in your UI
        self.pc.setValidator(dv(0.1, 5000.0, 3))          # bar (typical range)
        self.mr.setValidator(dv(0.1, 20.0, 4))           # O/F

        self.of_min.setValidator(dv(0.1, 50.0, 4))
        self.of_max.setValidator(dv(0.1, 50.0, 4))
        self.of_inc.setValidator(dv(0.001, 10.0, 4))

        # Nozzle / performance
        self.thrust.setValidator(dv(0.0, 1e8, 3))        # N

        self.amb.setValidator(dv(0.0, 50.0, 5))          # bar

        self.convergence_angle.setValidator(dv(1.0, 75.0, 2))  # deg
        self.divergence_angle.setValidator(dv(1.0, 60.0, 2))   # deg

        self.cr.setValidator(dv(1.0, 50.0, 3))           # Ac/At

        # "throat_ratio" is ambiguous; you currently allow e.g. 0.05.
        # Enforce positive; keep broad until you finalize meaning.
        self.throat_ratio.setValidator(dv(1e-6, 1e2, 6))

        self.lstar.setValidator(dv(0.01, 50.0, 4))       # m

    def set_plot_figures(self, figures: dict):
        self._figures = figures
        self._render_selected_plot()

    def _render_selected_plot(self):
        if not hasattr(self, "_figures") or not self._figures:
            return

        key = self.metric_combo.currentText()
        fig = self._figures.get(key)
        if fig is None:
            return

        # Clear old widgets from plot_widget_layout
        while self.plot_widget_layout.count():
            item = self.plot_widget_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Create new canvas + toolbar for this figure
        self._plot_canvas = FigureCanvas(fig)
        self._plot_toolbar = NavigationToolbar(self._plot_canvas, self)

        self.plot_widget_layout.addWidget(self._plot_toolbar)
        self.plot_widget_layout.addWidget(self._plot_canvas)

    def set_viz_figures(self, fig2d, fig3d):
        # --- 2D ---
        while self.viz2d_layout.count():
            item = self.viz2d_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        self._viz2d_canvas = FigureCanvas(fig2d)
        self._viz2d_toolbar = NavigationToolbar(self._viz2d_canvas, self)
        self.viz2d_layout.addWidget(self._viz2d_toolbar)
        self.viz2d_layout.addWidget(self._viz2d_canvas)

        # --- 3D ---
        while self.viz3d_layout.count():
            item = self.viz3d_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        self._viz3d_canvas = FigureCanvas(fig3d)
        self._viz3d_toolbar = NavigationToolbar(self._viz3d_canvas, self)
        self.viz3d_layout.addWidget(self._viz3d_toolbar)
        self.viz3d_layout.addWidget(self._viz3d_canvas)

    def _toggle_left(self):
        self.left_dock.setVisible(not self.left_dock.isVisible())

    def _toggle_right(self):
        self.right_dock.setVisible(not self.right_dock.isVisible())

    def _toggle_bottom(self):
        self.bottom_dock.setVisible(not self.bottom_dock.isVisible())

    def _about(self):
        QMessageBox.information(self, "About", "SolidWorks-style layout using QMainWindow + DockWidgets + Toolbars.")

    def _noop(self):
        self.statusBar().showMessage("Not implemented yet")

    def is_dark_mode(self) -> bool:
        # For plotting: treat dark and barbie as "dark" plots
        return self.theme_mode() in ("dark", "barbie")
    
    def theme_mode(self) -> str:
    # returns: "system" | "light" | "dark" | "barbie"
        return getattr(self, "_theme_mode", "system")

    def _apply_theme_mode(self, mode: str):
        self._theme_mode = mode

        if hasattr(self, "settings") and self.settings is not None:
            self.settings.setValue("theme/mode", mode)

        app = QApplication.instance()
        apply_theme(app, mode)

        if hasattr(self, "controller"):
            self.controller.on_theme_changed()

def createPopupMenu(self):
    return None