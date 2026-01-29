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
from widgets.search_box import SearchBox
from widgets.filter_dialog import FilterDialog
from services.search_service import SearchService


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self._setup_window()
        self._setup_search_bar()
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

        main_layout.addWidget(self.search_box)

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
        self.menu_bar.signals.view_show_hidden.connect(self._on_show_hidden)

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
        self.tool_bar.signals.search.connect(self.show_search_bar)
        self.tool_bar.signals.filter.connect(self.show_filter_dialog)

    def _setup_status_bar(self):
        """设置状态栏"""
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        self.sidebar_widget.signals.node_selected.connect(self._on_sidebar_selected)
        self.file_manager_widget.signals.file_selected.connect(self._on_file_selected)

    def _setup_search_bar(self):
        """设置搜索栏"""
        self.search_box = SearchBox(self)
        self.search_box.setVisible(False)
        self.search_box.search_changed.connect(self._on_search_changed)
        self.search_box.search_cleared.connect(self._on_search_cleared)

        self.search_service = SearchService()

        self.filter_dialog = FilterDialog(self)
        self.filter_dialog.filter_applied.connect(self._on_filter_applied)

    def _on_set_path(self):
        """处理设置路径事件"""
        dialog = SetPathDialog(parent=self)
        if dialog.exec():
            path = dialog.get_selected_path()
            self.sidebar_widget.load_tree(path)
            self.status_bar.set_path(path)

    def _on_new_folder(self):
        """处理新建文件夹事件"""
        from PySide6.QtWidgets import QInputDialog
        from services.folder_service import FolderService
        
        current_path = self.status_bar.get_path()
        if not current_path:
            return
        
        folder_name, ok = QInputDialog.getText(self, "新建文件夹", "请输入文件夹名称:")
        if ok and folder_name:
            folder_service = FolderService()
            try:
                folder_service.create_folder(current_path, folder_name)
                self._refresh_current_path()
                self.status_bar.set_operation(f"文件夹 '{folder_name}' 创建成功")
            except Exception as e:
                self.status_bar.set_operation(f"创建文件夹失败: {str(e)}")

    def _on_copy(self):
        """处理复制事件"""
        from utils.clipboard_manager import ClipboardManager
        
        current_path = self.status_bar.get_path()
        if not current_path:
            return
        
        selection = self.status_bar.get_selection()
        if not selection:
            return
        
        file_path = current_path + "\\" + selection if current_path[-1] != "\\" else current_path + selection
        
        clipboard_manager = ClipboardManager()
        clipboard_manager.copy_file(file_path)
        self.status_bar.set_operation(f"已复制: {selection}")

    def _on_paste(self):
        """处理粘贴事件"""
        from utils.clipboard_manager import ClipboardManager
        from services.file_service import FileService
        
        current_path = self.status_bar.get_path()
        if not current_path:
            return
        
        clipboard_manager = ClipboardManager()
        clipboard_data = clipboard_manager.get_clipboard_data()
        
        if clipboard_data and clipboard_data['action'] == 'copy':
            file_service = FileService()
            try:
                file_service.copy_file(clipboard_data['path'], current_path)
                self._refresh_current_path()
                self.status_bar.set_operation("粘贴成功")
            except Exception as e:
                self.status_bar.set_operation(f"粘贴失败: {str(e)}")

    def _on_cut(self):
        """处理剪切事件"""
        from utils.clipboard_manager import ClipboardManager
        
        current_path = self.status_bar.get_path()
        if not current_path:
            return
        
        selection = self.status_bar.get_selection()
        if not selection:
            return
        
        file_path = current_path + "\\" + selection if current_path[-1] != "\\" else current_path + selection
        
        clipboard_manager = ClipboardManager()
        clipboard_manager.cut_file(file_path)
        self.status_bar.set_operation(f"已剪切: {selection}")

    def _on_delete(self):
        """处理删除事件"""
        from PySide6.QtWidgets import QMessageBox
        from services.file_service import FileService
        from services.folder_service import FolderService
        from pathlib import Path
        
        current_path = self.status_bar.get_path()
        if not current_path:
            return
        
        selection = self.status_bar.get_selection()
        if not selection:
            return
        
        file_path = current_path + "\\" + selection if current_path[-1] != "\\" else current_path + selection
        
        reply = QMessageBox.question(
            self, 
            "确认删除", 
            f"确定要删除 '{selection}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if Path(file_path).is_dir():
                    folder_service = FolderService()
                    folder_service.delete_folder(file_path)
                else:
                    file_service = FileService()
                    file_service.delete_file(file_path)
                
                self._refresh_current_path()
                self.status_bar.set_operation(f"'{selection}' 已删除")
            except Exception as e:
                self.status_bar.set_operation(f"删除失败: {str(e)}")

    def _on_rename(self):
        """处理重命名事件"""
        from PySide6.QtWidgets import QInputDialog
        from services.file_service import FileService
        from services.folder_service import FolderService
        from pathlib import Path
        
        current_path = self.status_bar.get_path()
        if not current_path:
            return
        
        selection = self.status_bar.get_selection()
        if not selection:
            return
        
        file_path = current_path + "\\" + selection if current_path[-1] != "\\" else current_path + selection
        
        new_name, ok = QInputDialog.getText(self, "重命名", "请输入新名称:", text=selection)
        if ok and new_name and new_name != selection:
            try:
                if Path(file_path).is_dir():
                    folder_service = FolderService()
                    folder_service.rename_folder(file_path, new_name)
                else:
                    file_service = FileService()
                    file_service.rename_file(file_path, new_name)
                
                self._refresh_current_path()
                self.status_bar.set_operation(f"重命名成功: {selection} -> {new_name}")
            except Exception as e:
                self.status_bar.set_operation(f"重命名失败: {str(e)}")

    def _on_refresh(self):
        """处理刷新事件"""
        self._refresh_current_path()
        self.status_bar.set_operation("已刷新")

    def _on_up(self):
        """处理上一级事件"""
        from pathlib import Path
        
        current_path = self.status_bar.get_path()
        if not current_path:
            return
        
        parent_path = str(Path(current_path).parent)
        if parent_path != current_path:
            self.sidebar_widget.load_tree(parent_path)
            self.status_bar.set_path(parent_path)
    
    def _refresh_current_path(self):
        """刷新当前路径"""
        current_path = self.status_bar.get_path()
        if current_path:
            from services.file_service import FileService
            file_service = FileService()
            files = file_service.list_files(current_path)
            self.file_manager_widget.load_files(files)

    def _on_sidebar_selected(self, path: str):
        """处理侧边栏选择事件"""
        self.status_bar.set_path(path)

    def _on_show_hidden(self, show: bool):
        """
        处理显示隐藏文件事件

        Args:
            show: 是否显示隐藏文件
        """
        self.file_manager_widget.set_show_hidden(show)
        self.status_bar.set_operation(f"{'显示' if show else '隐藏'}隐藏文件")

    def _on_file_selected(self, file_path: str):
        """处理文件选择事件"""
        from pathlib import Path
        path = Path(file_path)
        self.status_bar.set_selection(f"{path.name}")

    def _on_search_changed(self, text: str):
        """
        处理搜索文本变化事件

        Args:
            text: 搜索文本
        """
        if text:
            current_path = self.status_bar.get_path()
            if current_path:
                results = self.search_service.search_files(current_path, text)
                self.file_manager_widget.load_files(results)
                self.status_bar.set_operation(f"找到 {len(results)} 个结果")

    def _on_search_cleared(self):
        """处理搜索清除事件"""
        current_path = self.status_bar.get_path()
        if current_path:
            from services.file_service import FileService
            file_service = FileService()
            files = file_service.list_files(current_path)
            self.file_manager_widget.load_files(files)
            self.status_bar.set_operation("")

    def _on_filter_applied(self, config: dict):
        """
        处理过滤应用事件

        Args:
            config: 过滤配置
        """
        self.file_manager_widget.set_filter_text(config.get('name', ''))
        self.file_manager_widget.set_show_hidden(config.get('show_hidden', False))

        file_type = config.get('type', '全部')
        if file_type == '文件夹':
            self.file_manager_widget.proxy_model.set_filter_folders(False)
            self.file_manager_widget.proxy_model.set_filter_files(True)
        elif file_type == '文件':
            self.file_manager_widget.proxy_model.set_filter_folders(True)
            self.file_manager_widget.proxy_model.set_filter_files(False)
        else:
            self.file_manager_widget.proxy_model.set_filter_folders(False)
            self.file_manager_widget.proxy_model.set_filter_files(False)

        self.status_bar.set_operation("过滤已应用")

    def show_search_bar(self):
        """显示搜索栏"""
        self.search_box.setVisible(True)
        self.search_box.set_focus()

    def hide_search_bar(self):
        """隐藏搜索栏"""
        self.search_box.setVisible(False)
        self.search_box.clear()

    def show_filter_dialog(self):
        """显示过滤对话框"""
        self.filter_dialog.exec()

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