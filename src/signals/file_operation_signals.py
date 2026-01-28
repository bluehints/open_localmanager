from PySide6.QtCore import QObject, Signal


class FileOperationSignals(QObject):
    """文件操作信号"""

    file_copied = Signal(str, str)
    file_moved = Signal(str, str)
    file_deleted = Signal(str)
    file_renamed = Signal(str, str)
    file_created = Signal(str)
    folder_created = Signal(str)
    folder_copied = Signal(str, str)
    folder_moved = Signal(str, str)
    folder_deleted = Signal(str)
    folder_renamed = Signal(str, str)
    operation_started = Signal(str)
    operation_finished = Signal(str, bool)
    operation_failed = Signal(str, str)