import os
from typing import Optional
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from .base_previewer import BasePreviewer


class ImagePreviewer(BasePreviewer):
    """图片预览器"""

    IMAGE_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
        '.webp', '.ico', '.svg', '.psd', '.raw', '.cr2', '.nef',
        '.orf', '.sr2', '.dng', '.arw', '.pef', '.raf', '.x3f'
    }

    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化图片预览器

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        self.widget = QWidget(self.parent)
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea(self.widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel(self.scroll_area)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("请选择图片文件进行预览")

        self.scroll_area.setWidget(self.image_label)
        layout.addWidget(self.scroll_area)

    def can_preview(self, file_path: str) -> bool:
        """
        判断是否可以预览该文件

        Args:
            file_path: 文件路径

        Returns:
            是否可以预览
        """
        if not os.path.isfile(file_path):
            return False

        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.IMAGE_EXTENSIONS

    def preview(self, file_path: str) -> bool:
        """
        预览文件

        Args:
            file_path: 文件路径

        Returns:
            预览是否成功
        """
        try:
            if not self.can_preview(file_path):
                return False

            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                return False

            scaled_pixmap = self._scale_pixmap(pixmap)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")
            self.current_path = file_path
            return True
        except Exception:
            return False

    def _scale_pixmap(self, pixmap: QPixmap) -> QPixmap:
        """
        缩放图片以适应显示区域

        Args:
            pixmap: 原始图片

        Returns:
            缩放后的图片
        """
        max_width = self.scroll_area.width() - 20
        max_height = self.scroll_area.height() - 20

        if pixmap.width() <= max_width and pixmap.height() <= max_height:
            return pixmap


        return pixmap.scaled(
            max_width,
            max_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def clear(self) -> None:
        """清空预览"""
        self.image_label.clear()
        self.image_label.setText("请选择图片文件进行预览")
        self.current_path = None

    def get_widget(self) -> QWidget:
        """
        获取预览窗口部件

        Returns:
            预览窗口部件
        """
        return self.widget