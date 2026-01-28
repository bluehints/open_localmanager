from typing import Optional, List
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QMimeData, QObject, Signal, QUrl
from PySide6.QtGui import QClipboard


class ClipboardManager(QObject):
    """剪贴板管理器"""

    clipboard_changed = Signal()

    def __init__(self):
        """初始化剪贴板管理器"""
        super().__init__()
        self.clipboard = QApplication.clipboard()
        self._setup_connections()

    def _setup_connections(self):
        """建立信号槽连接"""
        self.clipboard.dataChanged.connect(self._on_clipboard_changed)

    def _on_clipboard_changed(self):
        """剪贴板内容改变"""
        self.clipboard_changed.emit()

    def set_text(self, text: str) -> bool:
        """
        设置文本到剪贴板

        Args:
            text: 文本内容

        Returns:
            设置是否成功
        """
        try:
            self.clipboard.setText(text)
            return True
        except Exception:
            return False

    def get_text(self) -> Optional[str]:
        """
        获取剪贴板文本

        Returns:
            剪贴板文本
        """
        return self.clipboard.text()

    def set_files(self, file_paths: List[str]) -> bool:
        """
        设置文件路径到剪贴板

        Args:
            file_paths: 文件路径列表

        Returns:
            设置是否成功
        """
        try:
            mime_data = QMimeData()
            mime_data.setUrls([QUrl.fromLocalFile(path) for path in file_paths])
            self.clipboard.setMimeData(mime_data)
            return True
        except Exception:
            return False

    def get_files(self) -> List[str]:
        """
        获取剪贴板文件路径

        Returns:
            文件路径列表
        """
        urls = self.clipboard.mimeData().urls()
        return [url.toLocalFile() for url in urls if url.isLocalFile()]

    def clear(self) -> bool:
        """
        清空剪贴板

        Returns:
            清空是否成功
        """
        try:
            self.clipboard.clear()
            return True
        except Exception:
            return False

    def has_text(self) -> bool:
        """
        检查剪贴板是否有文本

        Returns:
            是否有文本
        """
        return bool(self.clipboard.text())

    def has_files(self) -> bool:
        """
        检查剪贴板是否有文件

        Returns:
            是否有文件
        """
        mime_data = self.clipboard.mimeData()
        return mime_data is not None and mime_data.hasUrls()

    def copy_text(self, text: str) -> bool:
        """
        复制文本

        Args:
            text: 文本内容

        Returns:
            复制是否成功
        """
        return self.set_text(text)

    def copy_files(self, file_paths: List[str]) -> bool:
        """
        复制文件

        Args:
            file_paths: 文件路径列表

        Returns:
            复制是否成功
        """
        return self.set_files(file_paths)

    def paste_text(self) -> Optional[str]:
        """
        粘贴文本

        Returns:
            粘贴的文本
        """
        return self.get_text()

    def paste_files(self) -> List[str]:
        """
        粘贴文件

        Returns:
            文件路径列表
        """
        return self.get_files()

    def get_mime_data(self) -> Optional[QMimeData]:
        """
        获取剪贴板MIME数据

        Returns:
            MIME数据
        """
        return self.clipboard.mimeData()

    def set_mime_data(self, mime_data: QMimeData) -> bool:
        """
        设置MIME数据到剪贴板

        Args:
            mime_data: MIME数据

        Returns:
            设置是否成功
        """
        try:
            self.clipboard.setMimeData(mime_data)
            return True
        except Exception:
            return False