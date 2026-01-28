from PySide6.QtCore import QObject, Signal
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from services.preview_service import PreviewService


class PreviewController(QObject):
    """
    预览区控制器
    处理预览区的业务逻辑
    """

    def __init__(self, preview_widget, preview_service: PreviewService):
        """
        初始化控制器

        Args:
            preview_widget: 预览区组件
            preview_service: 预览服务
        """
        super().__init__()
        self.preview_widget = preview_widget
        self.preview_service = preview_service
        self._setup_connections()

    def _setup_connections(self):
        """建立信号槽连接"""
        self.preview_service.signals.preview_loaded.connect(self._on_preview_loaded)
        self.preview_service.signals.preview_failed.connect(self._on_preview_failed)

    def _on_preview_loaded(self, file_path: str):
        """
        处理预览加载完成事件

        Args:
            file_path: 文件路径
        """
        pass

    def _on_preview_failed(self, file_path: str, error: str):
        """
        处理预览失败事件

        Args:
            file_path: 文件路径
            error: 错误信息
        """
        pass

    def preview_file(self, file_path: str):
        """
        预览文件

        Args:
            file_path: 文件路径
        """
        try:
            self.preview_service.preview_file(file_path, self.preview_widget)
        except Exception as e:
            pass

    def clear_preview(self):
        """清除预览"""
        try:
            self.preview_service.clear_preview(self.preview_widget)
        except Exception as e:
            pass

    def zoom_in(self):
        """放大"""
        pass

    def zoom_out(self):
        """缩小"""
        pass

    def reset_zoom(self):
        """重置缩放"""
        pass