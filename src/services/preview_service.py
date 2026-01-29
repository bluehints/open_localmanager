from typing import Optional
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QObject, Signal, Qt
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from previewers.base_previewer import BasePreviewer
from previewers.previewer_factory import PreviewerFactory


class PreviewService(QObject):
    """预览服务"""

    preview_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化预览服务

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.parent = parent
        self.factory = PreviewerFactory(parent)
        self.current_previewer: Optional[BasePreviewer] = None
        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        self.widget = QWidget(self.parent)
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget(self.widget)
        layout.addWidget(self.stacked_widget)

        self.no_preview_label = QLabel("请选择文件进行预览", self.stacked_widget)
        self.no_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_preview_label.setStyleSheet("color: #999; font-size: 14px;")
        self.stacked_widget.addWidget(self.no_preview_label)

        for previewer in self.factory.get_all_previewers():
            self.stacked_widget.addWidget(previewer.get_widget())

    def preview_file(self, file_path: str) -> bool:
        """
        预览文件

        Args:
            file_path: 文件路径

        Returns:
            预览是否成功
        """
        try:
            if self.current_previewer:
                self.current_previewer.clear()

            previewer = self.factory.get_previewer(file_path)
            if not previewer:
                self._show_no_preview()
                return False

            if previewer.preview(file_path):
                self.current_previewer = previewer
                self._show_previewer(previewer)
                self.preview_changed.emit(file_path)
                return True
            else:
                self._show_no_preview()
                return False
        except Exception:
            self._show_no_preview()
            return False

    def clear_preview(self) -> None:
        """清空预览"""
        if self.current_previewer:
            self.current_previewer.clear()
            self.current_previewer = None
        self._show_no_preview()

    def _show_previewer(self, previewer: BasePreviewer) -> None:
        """
        显示预览器

        Args:
            previewer: 预览器实例
        """
        widget = previewer.get_widget()
        index = self.stacked_widget.indexOf(widget)
        if index >= 0:
            self.stacked_widget.setCurrentIndex(index)

    def _show_no_preview(self) -> None:
        """显示无预览界面"""
        self.stacked_widget.setCurrentWidget(self.no_preview_label)

    def can_preview(self, file_path: str) -> bool:
        """
        判断是否可以预览该文件

        Args:
            file_path: 文件路径

        Returns:
            是否可以预览
        """
        return self.factory.can_preview(file_path)

    def get_supported_extensions(self):
        """
        获取所有支持的文件扩展名

        Returns:
            扩展名列表
        """
        return self.factory.get_supported_extensions()

    def get_widget(self) -> QWidget:
        """
        获取预览服务窗口部件

        Returns:
            窗口部件
        """
        return self.widget

    def get_current_path(self) -> Optional[str]:
        """
        获取当前预览的文件路径

        Returns:
            当前文件路径
        """
        if self.current_previewer:
            return self.current_previewer.get_current_path()
        return None