from PySide6.QtCore import QObject
import sys
from pathlib import Path
import os
sys.path.insert(0, str(Path(__file__).parent.parent))
from signals.main_window_signals import MainWindowSignals
from services.file_service import FileService
from models.file_item import FileItem


class MainWindowController(QObject):
    """主窗口控制器"""

    def __init__(self, main_window):
        """
        初始化主窗口控制器

        Args:
            main_window: 主窗口实例
        """
        super().__init__()
        self.main_window = main_window
        self.signals = MainWindowSignals()
        self.file_service = FileService()
        self._setup_connections()
        self._initialize_ui()

    def _setup_connections(self):
        """建立信号槽连接"""
        sidebar = self.main_window.sidebar_widget
        file_manager = self.main_window.file_manager_widget
        preview_service = self.main_window.preview_service

        sidebar.signals.node_selected.connect(self._on_sidebar_selected)
        file_manager.signals.file_selected.connect(self._on_file_selected)
        file_manager.signals.file_double_clicked.connect(self._on_file_double_clicked)

    def _initialize_ui(self):
        """初始化用户界面"""
        import os
        root_path = os.path.expanduser("~")
        self.main_window.sidebar_widget.load_tree(root_path)

    def _on_sidebar_selected(self, path: str):
        """
        处理侧边栏选择事件

        Args:
            path: 选中的路径
        """
        try:
            files = []
            for entry in os.listdir(path):
                entry_path = os.path.join(path, entry)
                if os.path.isfile(entry_path):
                    stat = os.stat(entry_path)
                    file_info = FileItem(
                        path=entry_path,
                        name=entry,
                        size=stat.st_size,
                        modified_time=stat.st_mtime,
                        file_type="文件"
                    )
                    files.append(file_info)
            self.main_window.file_manager_widget.load_files(files)
        except Exception:
            pass

    def _on_file_selected(self, file_path: str):
        """
        处理文件选择事件

        Args:
            file_path: 选中的文件路径
        """
        self.main_window.preview_service.preview_file(file_path)

    def _on_file_double_clicked(self, file_path: str):
        """
        处理文件双击事件

        Args:
            file_path: 双击的文件路径
        """
        self.main_window.preview_service.preview_file(file_path)

    def handle_sidebar_selection(self, path: str):
        """
        处理侧边栏选择事件

        Args:
            path: 选中的路径
        """
        self.signals.sidebar_selected.emit(path)

    def handle_file_selection(self, file_path: str):
        """
        处理文件选择事件

        Args:
            file_path: 选中的文件路径
        """
        self.signals.file_selected.emit(file_path)

    def handle_file_operation(self, operation: str, *args):
        """
        处理文件操作事件

        Args:
            operation: 操作类型
            *args: 操作参数
        """
        self.signals.file_operation.emit(operation, args)

    def update_ui(self):
        """更新用户界面"""
        pass