from PySide6.QtCore import QObject, Signal


class PreviewSignals(QObject):
    """预览区信号"""

    preview_loaded = Signal(str)
    preview_failed = Signal(str, str)
    zoom_changed = Signal(float)