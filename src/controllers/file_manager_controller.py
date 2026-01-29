from PySide6.QtCore import QObject, Signal
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from services.file_service import FileService


class FileManagerController(QObject):
    """
    文件管理区控制器
    处理文件管理区的业务逻辑
    """

    def __init__(self, file_manager_widget, file_service: FileService):
        """
        初始化控制器

        Args:
            file_manager_widget: 文件管理区组件
            file_service: 文件服务
        """
        super().__init__()
        self.file_manager_widget = file_manager_widget
        self.file_service = file_service
        self._setup_connections()

    def _setup_connections(self):
        """建立信号槽连接"""
        self.file_manager_widget.signals.file_selected.connect(self._on_file_selected)
        self.file_manager_widget.signals.file_double_clicked.connect(self._on_file_double_clicked)
        self.file_manager_widget.signals.context_menu_requested.connect(self._on_context_menu_requested)
        self.file_manager_widget.signals.sort_changed.connect(self._on_sort_changed)
        self.file_manager_widget.signals.filter_changed.connect(self._on_filter_changed)

    def _on_file_selected(self, file_path: str):
        """
        处理文件选择事件

        Args:
            file_path: 文件路径
        """
        pass

    def _on_file_double_clicked(self, file_path: str):
        """
        处理文件双击事件

        Args:
            file_path: 文件路径
        """
        pass

    def _on_context_menu_requested(self, file_path: str, position):
        """
        处理右键菜单请求事件

        Args:
            file_path: 文件路径
            position: 位置
        """
        pass

    def _on_sort_changed(self, column: int, order):
        """
        处理排序变更事件

        Args:
            column: 列号
            order: 排序顺序
        """
        pass

    def _on_filter_changed(self, filter_text: str):
        """
        处理过滤变更事件

        Args:
            filter_text: 过滤文本
        """
        pass

    def sync_with_sidebar(self, folder_path: str):
        """
        与侧边栏同步

        Args:
            folder_path: 文件夹路径
        """
        try:
            files = self.file_service.list_files(folder_path)
            self.file_manager_widget.load_files(files)
        except Exception as e:
            pass

    def load_folder(self, folder_path: str):
        """
        加载文件夹

        Args:
            folder_path: 文件夹路径
        """
        self.sync_with_sidebar(folder_path)