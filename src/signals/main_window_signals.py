from PySide6.QtCore import QObject, Signal


class MainWindowSignals(QObject):
    """主窗口信号"""

    sidebar_selected = Signal(str)
    file_selected = Signal(str)
    file_operation = Signal(str, object)
    config_changed = Signal(dict)