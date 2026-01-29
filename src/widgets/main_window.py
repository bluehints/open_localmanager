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


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self._setup_window()
        self._setup_ui()
        self._setup_menu_bar()
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

    def _on_set_path(self):
        """处理设置路径事件"""
        dialog = SetPathDialog(parent=self)
        if dialog.exec():
            path = dialog.get_selected_path()
            self.sidebar_widget.load_tree(path)

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