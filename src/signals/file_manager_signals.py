from PySide6.QtCore import QObject, Signal, QPoint, Qt


class FileManagerSignals(QObject):
    """文件管理区信号"""

    file_selected = Signal(str)
    file_double_clicked = Signal(str)
    context_menu_requested = Signal(str, QPoint)
    sort_changed = Signal(int, Qt.SortOrder)
    filter_changed = Signal(str)