from PySide6.QtCore import QObject, Signal, QPoint


class SidebarSignals(QObject):
    """侧边栏信号"""

    node_expanded = Signal(str)
    node_collapsed = Signal(str)
    node_selected = Signal(str)
    context_menu_requested = Signal(str, QPoint)