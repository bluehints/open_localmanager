from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter
)
from PySide6.QtCore import Qt
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from controllers.main_window_controller import MainWindowController
from widgets.sidebar_widget import SidebarWidget
from widgets.file_manager_widget import FileManagerWidget
from services.preview_service import PreviewService
from widgets.menu_bar import MenuBar
from widgets.set_path_dialog import SetPathDialog
from widgets.status_bar import StatusBar
from widgets.tool_bar import ToolBar


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self._setup_window()
        self._setup_ui()
        self._setup_menu_bar()
        self._setup_tool_bar()
        self._setup_status_bar()
        self.controller = MainWindowController(self)

    def _setup_window(self):
        """设置窗口属性"""
        self.setWindowTitle("Open资料助手")
        self.setMinimumSize(1200, 800)
        self.resize(1200, 800)

    def _setup_ui(self):
        """设置用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        self.sidebar_widget = SidebarWidget(splitter)
        self.sidebar_widget.setMinimumWidth(200)
        self.sidebar_widget.setMaximumWidth(400)
        splitter.addWidget(self.sidebar_widget)

        self.file_manager_widget = FileManagerWidget(splitter)
        splitter.addWidget(self.file_manager_widget)

        self.preview_service = PreviewService(splitter)
        self.preview_widget = self.preview_service.get_widget()
        self.preview_widget.setMinimumWidth(300)
        self.preview_widget.setMaximumWidth(500)
        splitter.addWidget(self.preview_widget)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 2)

    def _setup_menu_bar(self):
        """设置菜单栏"""
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        self.menu_bar.signals.tools_set_path.connect(self._on_set_path)

    def _setup_tool_bar(self):
        """设置工具栏"""
        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)
        
        self.tool_bar.signals.new_folder.connect(self._on_new_folder)
        self.tool_bar.signals.copy.connect(self._on_copy)
        self.tool_bar.signals.paste.connect(self._on_paste)
        self.tool_bar.signals.cut.connect(self._on_cut)
        self.tool_bar.signals.delete.connect(self._on_delete)
        self.tool_bar.signals.rename.connect(self._on_rename)
        self.tool_bar.signals.refresh.connect(self._on_refresh)
        self.tool_bar.signals.up.connect(self._on_up)

    def _setup_status_bar(self):
        """设置状态栏"""
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        self.sidebar_widget.signals.node_selected.connect(self._on_sidebar_selected)
        self.file_manager_widget.signals.file_selected.connect(self._on_file_selected)

    def _on_set_path(self):
        """处理设置路径事件"""
        dialog = SetPathDialog(parent=self)
        if dialog.exec():
            path = dialog.get_selected_path()
            self.sidebar_widget.load_tree(path)
            self.status_bar.set_path(path)

    def _on_new_folder(self):
        """处理新建文件夹事件"""
        pass

    def _on_copy(self):
        """处理复制事件"""
        pass

    def _on_paste(self):
        """处理粘贴事件"""
        pass

    def _on_cut(self):
        """处理剪切事件"""
        pass

    def _on_delete(self):
        """处理删除事件"""
        pass

    def _on_rename(self):
        """处理重命名事件"""
        pass

    def _on_refresh(self):
        """处理刷新事件"""
        pass

    def _on_up(self):
        """处理上一级事件"""
        pass

    def _on_sidebar_selected(self, path: str):
        """处理侧边栏选择事件"""
        self.status_bar.set_path(path)

    def _on_file_selected(self, file_path: str):
        """处理文件选择事件"""
        from pathlib import Path
        path = Path(file_path)
        self.status_bar.set_selection(f"{path.name}")

    def load_config(self):
        """加载配置"""
        pass

    def save_config(self):
        """保存配置"""
        pass

    def closeEvent(self, event):
        """
        窗口关闭事件处理

        Args:
            event: 关闭事件
        """
        self.save_config()
        event.accept()