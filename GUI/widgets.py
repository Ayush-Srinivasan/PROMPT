from PySide6.QtWidgets import QComboBox, QCompleter
from PySide6.QtCore import Qt

def make_searchable(combo: QComboBox) -> None:
    combo.setEditable(True)
    combo.setInsertPolicy(QComboBox.NoInsert)

    completer = combo.completer()
    completer.setCompletionMode(QCompleter.PopupCompletion)
    completer.setFilterMode(Qt.MatchContains)  # match anywhere, not just prefix
    completer.setCaseSensitivity(Qt.CaseInsensitive)