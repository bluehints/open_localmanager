import os
from typing import Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from .base_previewer import BasePreviewer


class PDFPreviewer(BasePreviewer):
    """PDF预览器"""

    PDF_EXTENSIONS = {'.pdf'}

    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化PDF预览器

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.current_page = 0
        self.total_pages = 0
        self.pdf_images = []
        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        self.widget = QWidget(self.parent)
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)

        control_layout = QHBoxLayout()

        self.prev_button = QPushButton("上一页", self.widget)
        self.prev_button.clicked.connect(self._prev_page)
        self.prev_button.setEnabled(False)
        control_layout.addWidget(self.prev_button)

        self.page_label = QLabel("第 0 / 0 页", self.widget)
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(self.page_label)

        self.next_button = QPushButton("下一页", self.widget)
        self.next_button.clicked.connect(self._next_page)
        self.next_button.setEnabled(False)
        control_layout.addWidget(self.next_button)

        layout.addLayout(control_layout)

        self.scroll_area = QScrollArea(self.widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel(self.scroll_area)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("请选择PDF文件进行预览")

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
        return ext.lower() in self.PDF_EXTENSIONS

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

            self._load_pdf(file_path)
            self.current_path = file_path
            return True
        except Exception:
            return False

    def _load_pdf(self, file_path: str):
        """
        加载PDF文件

        Args:
            file_path: PDF文件路径
        """
        try:
            import fitz

            doc = fitz.open(file_path)
            self.total_pages = len(doc)
            self.pdf_images = []

            for page_num in range(self.total_pages):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(img)
                self.pdf_images.append(pixmap)

            doc.close()

            self.current_page = 0
            self._update_display()
        except ImportError:
            self.image_label.setText("需要安装PyMuPDF库来预览PDF文件\n请运行: pip install PyMuPDF")
        except Exception as e:
            self.image_label.setText(f"加载PDF失败: {str(e)}")

    def _update_display(self):
        """更新显示"""
        if self.pdf_images and self.current_page < len(self.pdf_images):
            pixmap = self.pdf_images[self.current_page]
            scaled_pixmap = self._scale_pixmap(pixmap)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")
            self.page_label.setText(f"第 {self.current_page + 1} / {self.total_pages} 页")

            self.prev_button.setEnabled(self.current_page > 0)
            self.next_button.setEnabled(self.current_page < self.total_pages - 1)
        else:
            self.image_label.setText("无法显示PDF内容")
            self.page_label.setText("第 0 / 0 页")
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)

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

    def _prev_page(self):
        """上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_display()

    def _next_page(self):
        """下一页"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._update_display()

    def clear(self) -> None:
        """清空预览"""
        self.image_label.clear()
        self.image_label.setText("请选择PDF文件进行预览")
        self.pdf_images = []
        self.current_page = 0
        self.total_pages = 0
        self.page_label.setText("第 0 / 0 页")
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.current_path = None

    def get_widget(self) -> QWidget:
        """
        获取预览窗口部件

        Returns:
            预览窗口部件
        """
        return self.widget