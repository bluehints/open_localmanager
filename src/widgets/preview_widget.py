from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel
)
from PySide6.QtCore import Qt
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from signals.preview_signals import PreviewSignals


class PreviewWidget(QWidget):
    """文件预览区组件"""

    def __init__(self, parent=None):
        """
        初始化预览区

        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self.signals = PreviewSignals()
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.preview_label = QLabel("请选择文件进行预览")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("color: gray; font-size: 14px;")
        layout.addWidget(self.preview_label)

        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setVisible(False)
        layout.addWidget(self.text_preview)

        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setVisible(False)
        layout.addWidget(self.image_preview)

    def _setup_connections(self):
        """建立信号槽连接"""
        pass

    def preview_text(self, content: str):
        """
        预览文本内容

        Args:
            content: 文本内容
        """
        self.preview_label.setVisible(False)
        self.image_preview.setVisible(False)
        self.text_preview.setVisible(True)
        self.text_preview.setPlainText(content)
        self.signals.preview_loaded.emit("text")

    def preview_image(self, pixmap):
        """
        预览图片内容

        Args:
            pixmap: 图片
        """
        self.preview_label.setVisible(False)
        self.text_preview.setVisible(False)
        self.image_preview.setVisible(True)
        self.image_preview.setPixmap(pixmap.scaled(
            self.image_preview.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.signals.preview_loaded.emit("image")

    def clear_preview(self):
        """清除预览"""
        self.preview_label.setVisible(True)
        self.text_preview.setVisible(False)
        self.image_preview.setVisible(False)
        self.text_preview.clear()
        self.image_preview.clear()

    def zoom_in(self):
        """放大"""
        if self.image_preview.isVisible():
            pixmap = self.image_preview.pixmap()
            if pixmap:
                scaled_pixmap = pixmap.scaled(
                    int(pixmap.width() * 1.2),
                    int(pixmap.height() * 1.2),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_preview.setPixmap(scaled_pixmap)
                self.signals.zoom_changed.emit(1.2)

    def zoom_out(self):
        """缩小"""
        if self.image_preview.isVisible():
            pixmap = self.image_preview.pixmap()
            if pixmap:
                scaled_pixmap = pixmap.scaled(
                    int(pixmap.width() * 0.8),
                    int(pixmap.height() * 0.8),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_preview.setPixmap(scaled_pixmap)
                self.signals.zoom_changed.emit(0.8)

    def reset_zoom(self):
        """重置缩放"""
        if self.image_preview.isVisible():
            pixmap = self.image_preview.pixmap()
            if pixmap:
                self.image_preview.setPixmap(pixmap)
                self.signals.zoom_changed.emit(1.0)