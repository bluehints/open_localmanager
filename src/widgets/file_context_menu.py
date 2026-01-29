from PySide6.QtWidgets import QMenu, QAction
from PySide6.QtCore import QObject, Signal, QPoint
from typing import Optional


class FileContextMenu(QObject):
    """文件右键菜单"""

    action_triggered = Signal(str, str)

    def __init__(self, parent=None):
        """
        初始化文件右键菜单

        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self._menu = QMenu(parent)
        self._current_path: Optional[str] = None
        self._is_folder = False
        self._setup_menu()

    def _setup_menu(self):
        """设置菜单"""
        self._open_action = QAction("打开", self._menu)
        self._open_action.triggered.connect(lambda: self._on_action("open"))
        self._menu.addAction(self._open_action)

        self._menu.addSeparator()

        self._copy_action = QAction("复制", self._menu)
        self._copy_action.triggered.connect(lambda: self._on_action("copy"))
        self._menu.addAction(self._copy_action)

        self._cut_action = QAction("剪切", self._menu)
        self._cut_action.triggered.connect(lambda: self._on_action("cut"))
        self._menu.addAction(self._cut_action)

        self._paste_action = QAction("粘贴", self._menu)
        self._paste_action.triggered.connect(lambda: self._on_action("paste"))
        self._menu.addAction(self._paste_action)

        self._menu.addSeparator()

        self._rename_action = QAction("重命名", self._menu)
        self._rename_action.triggered.connect(lambda: self._on_action("rename"))
        self._menu.addAction(self._rename_action)

        self._delete_action = QAction("删除", self._menu)
        self._delete_action.triggered.connect(lambda: self._on_action("delete"))
        self._menu.addAction(self._delete_action)

        self._menu.addSeparator()

        self._properties_action = QAction("属性", self._menu)
        self._properties_action.triggered.connect(lambda: self._on_action("properties"))
        self._menu.addAction(self._properties_action)

    def _on_action(self, action_type: str):
        """
        处理菜单动作

        Args:
            action_type: 动作类型
        """
        if self._current_path:
            self.action_triggered.emit(action_type, self._current_path)

    def show_menu(self, position: QPoint, path: str, is_folder: bool = False):
        """
        显示菜单

        Args:
            position: 位置
            path: 路径
            is_folder: 是否是文件夹
        """
        self._current_path = path
        self._is_folder = is_folder

        self._paste_action.setVisible(is_folder)

        self._menu.exec_(position)

    def get_menu(self) -> QMenu:
        """
        获取菜单

        Returns:
            菜单
        """
        return self._menu