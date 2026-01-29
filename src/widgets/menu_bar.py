from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QObject, Signal


class MenuBarSignals(QObject):
    """菜单栏信号"""

    file_new_folder = Signal()
    file_new_file = Signal()
    file_open = Signal()
    file_save = Signal()
    file_exit = Signal()
    edit_copy = Signal()
    edit_paste = Signal()
    edit_cut = Signal()
    edit_delete = Signal()
    edit_rename = Signal()
    view_refresh = Signal()
    view_show_hidden = Signal(bool)
    tools_set_path = Signal()
    help_about = Signal()


class MenuBar(QMenuBar):
    """菜单栏组件"""

    def __init__(self, parent=None):
        """
        初始化菜单栏

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.signals = MenuBarSignals()
        self._setup_menus()

    def _setup_menus(self):
        """设置菜单"""
        self._setup_file_menu()
        self._setup_edit_menu()
        self._setup_view_menu()
        self._setup_tools_menu()
        self._setup_help_menu()

    def _setup_file_menu(self):
        """设置文件菜单"""
        file_menu = self.addMenu("文件(&F)")

        new_folder_action = QAction("新建文件夹(&N)", self)
        new_folder_action.setShortcut("Ctrl+Shift+N")
        new_folder_action.triggered.connect(self.signals.file_new_folder.emit)
        file_menu.addAction(new_folder_action)

        new_file_action = QAction("新建文件(&F)", self)
        new_file_action.setShortcut("Ctrl+N")
        new_file_action.triggered.connect(self.signals.file_new_file.emit)
        file_menu.addAction(new_file_action)

        file_menu.addSeparator()

        open_action = QAction("打开(&O)", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.signals.file_open.emit)
        file_menu.addAction(open_action)

        save_action = QAction("保存(&S)", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.signals.file_save.emit)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.signals.file_exit.emit)
        file_menu.addAction(exit_action)

    def _setup_edit_menu(self):
        """设置编辑菜单"""
        edit_menu = self.addMenu("编辑(&E)")

        copy_action = QAction("复制(&C)", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.signals.edit_copy.emit)
        edit_menu.addAction(copy_action)

        paste_action = QAction("粘贴(&V)", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.signals.edit_paste.emit)
        edit_menu.addAction(paste_action)

        cut_action = QAction("剪切(&T)", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.signals.edit_cut.emit)
        edit_menu.addAction(cut_action)

        edit_menu.addSeparator()

        delete_action = QAction("删除(&D)", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.signals.edit_delete.emit)
        edit_menu.addAction(delete_action)

        rename_action = QAction("重命名(&R)", self)
        rename_action.setShortcut("F2")
        rename_action.triggered.connect(self.signals.edit_rename.emit)
        edit_menu.addAction(rename_action)

    def _setup_view_menu(self):
        """设置视图菜单"""
        view_menu = self.addMenu("视图(&V)")

        refresh_action = QAction("刷新(&R)", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.signals.view_refresh.emit)
        view_menu.addAction(refresh_action)

        view_menu.addSeparator()

        show_hidden_action = QAction("显示隐藏文件(&H)", self)
        show_hidden_action.setCheckable(True)
        show_hidden_action.triggered.connect(self.signals.view_show_hidden.emit)
        view_menu.addAction(show_hidden_action)

    def _setup_tools_menu(self):
        """设置工具菜单"""
        tools_menu = self.addMenu("工具(&T)")

        set_path_action = QAction("设置管理路径(&S)", self)
        set_path_action.triggered.connect(self.signals.tools_set_path.emit)
        tools_menu.addAction(set_path_action)

    def _setup_help_menu(self):
        """设置帮助菜单"""
        help_menu = self.addMenu("帮助(&H)")

        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self.signals.help_about.emit)
        help_menu.addAction(about_action)