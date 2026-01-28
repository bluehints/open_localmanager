from typing import Optional, List
from PySide6.QtWidgets import QWidget
from .base_previewer import BasePreviewer
from .text_previewer import TextPreviewer
from .image_previewer import ImagePreviewer
from .video_previewer import VideoPreviewer
from .audio_previewer import AudioPreviewer
from .pdf_previewer import PDFPreviewer


class PreviewerFactory:
    """预览器工厂"""

    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化预览器工厂

        Args:
            parent: 父窗口
        """
        self.parent = parent
        self._previewers: List[BasePreviewer] = []
        self._initialize_previewers()

    def _initialize_previewers(self):
        """初始化所有预览器"""
        self._previewers = [
            TextPreviewer(self.parent),
            ImagePreviewer(self.parent),
            VideoPreviewer(self.parent),
            AudioPreviewer(self.parent),
            PDFPreviewer(self.parent)
        ]

    def get_previewer(self, file_path: str) -> Optional[BasePreviewer]:
        """
        根据文件路径获取合适的预览器

        Args:
            file_path: 文件路径

        Returns:
            预览器实例，如果没有合适的预览器则返回None
        """
        for previewer in self._previewers:
            if previewer.can_preview(file_path):
                return previewer
        return None

    def get_supported_extensions(self) -> List[str]:
        """
        获取所有支持的文件扩展名

        Returns:
            扩展名列表
        """
        extensions = set()
        for previewer in self._previewers:
            if hasattr(previewer, 'TEXT_EXTENSIONS'):
                extensions.update(previewer.TEXT_EXTENSIONS)
            elif hasattr(previewer, 'IMAGE_EXTENSIONS'):
                extensions.update(previewer.IMAGE_EXTENSIONS)
            elif hasattr(previewer, 'VIDEO_EXTENSIONS'):
                extensions.update(previewer.VIDEO_EXTENSIONS)
            elif hasattr(previewer, 'AUDIO_EXTENSIONS'):
                extensions.update(previewer.AUDIO_EXTENSIONS)
            elif hasattr(previewer, 'PDF_EXTENSIONS'):
                extensions.update(previewer.PDF_EXTENSIONS)
        return sorted(list(extensions))

    def can_preview(self, file_path: str) -> bool:
        """
        判断是否可以预览该文件

        Args:
            file_path: 文件路径

        Returns:
            是否可以预览
        """
        return self.get_previewer(file_path) is not None

    def get_all_previewers(self) -> List[BasePreviewer]:
        """
        获取所有预览器

        Returns:
            预览器列表
        """
        return self._previewers.copy()