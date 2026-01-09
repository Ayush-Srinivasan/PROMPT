from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication


def apply_system_theme(app: QApplication) -> None:
    app.setPalette(app.style().standardPalette())


def apply_light_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(242, 242, 242))
    palette.setColor(QPalette.WindowText, QColor(20, 20, 20))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(235, 235, 235))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(20, 20, 20))
    palette.setColor(QPalette.Text, QColor(20, 20, 20))
    palette.setColor(QPalette.Button, QColor(245, 245, 245))
    palette.setColor(QPalette.ButtonText, QColor(20, 20, 20))
    palette.setColor(QPalette.BrightText, QColor(200, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(31, 119, 180))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)


def apply_dark_theme(app: QApplication) -> None:
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app.setPalette(palette)


def apply_barbie_theme(app: QApplication) -> None:
    app.setStyle("Fusion")

    BG = QColor("#1A0F14")        # Dark Barbie Night
    PANEL = QColor("#2A1821")     # Panel Pink Charcoal
    TEXT = QColor("#FFF0F6")      # Cream White
    TEXT_MUTED = QColor("#C9A3B4")# Muted Rose Gray
    BORDER = QColor("#6A2E4F")    # Outline / Borders
    PINK = QColor("#E0218A")      # Barbie Pink accent

    palette = QPalette()
    palette.setColor(QPalette.Window, BG)
    palette.setColor(QPalette.WindowText, TEXT)

    palette.setColor(QPalette.Base, PANEL)
    palette.setColor(QPalette.AlternateBase, BG)

    palette.setColor(QPalette.ToolTipBase, TEXT)
    palette.setColor(QPalette.ToolTipText, BG)

    palette.setColor(QPalette.Text, TEXT)
    palette.setColor(QPalette.PlaceholderText, TEXT_MUTED)

    palette.setColor(QPalette.Button, PANEL)
    palette.setColor(QPalette.ButtonText, TEXT)

    palette.setColor(QPalette.BrightText, QColor(255, 0, 80))
    palette.setColor(QPalette.Highlight, PINK)
    palette.setColor(QPalette.HighlightedText, QColor("#1A0F14"))

    # Some controls use these roles:
    palette.setColor(QPalette.Light, BORDER)
    palette.setColor(QPalette.Mid, BORDER)
    palette.setColor(QPalette.Dark, BORDER)

    app.setPalette(palette)

def apply_brat_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    
    BG = QColor("#0F120A")          # Deep olive-black background
    PANEL = QColor("#1E2314")       # Olive panel
    TEXT = QColor("#E6ECD8")        # Soft off-white
    TEXT_MUTED = QColor("#A7B39A")  # Muted sage
    BORDER = QColor("#2A301A")      # Subtle olive border
    GREEN = QColor("#8ACE00")       # Brat Green primary
    '''
    BG = QColor("#8ACE00")          
    PANEL = QColor("#8ACE00")       # BRAT GREEN PANELS
    TEXT = QColor("#0A0A00")        # Near-black text
    TEXT_MUTED = QColor("#2A2A00")
    BORDER = QColor("#8ACE00")      # Laser green borders
    GREEN = QColor("#8ACE00")   # Full-on green highlight
    '''
    palette = QPalette()
    palette.setColor(QPalette.Window, BG)
    palette.setColor(QPalette.WindowText, TEXT)

    palette.setColor(QPalette.Base, PANEL)
    palette.setColor(QPalette.AlternateBase, BG)

    palette.setColor(QPalette.ToolTipBase, TEXT)
    palette.setColor(QPalette.ToolTipText, BG)

    palette.setColor(QPalette.Text, TEXT)
    palette.setColor(QPalette.PlaceholderText, TEXT_MUTED)

    palette.setColor(QPalette.Button, PANEL)
    palette.setColor(QPalette.ButtonText, TEXT)

    palette.setColor(QPalette.BrightText, QColor("#A6F200"))
    palette.setColor(QPalette.Highlight, GREEN)
    palette.setColor(QPalette.HighlightedText, BG)

    # Structural roles (borders, separators)
    palette.setColor(QPalette.Light, BORDER)
    palette.setColor(QPalette.Mid, BORDER)
    palette.setColor(QPalette.Dark, BORDER)

    app.setPalette(palette)

def apply_theme(app: QApplication, mode: str) -> None:
    mode = (mode or "system").strip().lower()
    if mode == "dark":
        apply_dark_theme(app)
    elif mode == "light":
        apply_light_theme(app)
    elif mode == "barbie":
        apply_barbie_theme(app)
    elif mode == "brat":
        apply_brat_theme(app)
    else:
        apply_system_theme(app)