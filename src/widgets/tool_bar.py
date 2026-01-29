from PySide6.QtWidgets import QToolBar, QStyle
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject, Signal, QSize
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


class ToolBarSignals(QObject):
    """工具栏信号"""

    new_folder = Signal()
    copy = Signal()
    paste = Signal()
    cut = Signal()
    delete = Signal()
    rename = Signal()
    refresh = Signal()
    up = Signal()
    back = Signal()
    forward = Signal()
    view_list = Signal()
    view_detail = Signal()
    view_icon = Signal()
    search = Signal()
    filter = Signal()


class ToolBar(QToolBar):
    """工具栏组件"""

    def __init__(self, parent=None):
        """
        初始化工具栏

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.signals = ToolBarSignals()
        self._load_icons()
        self._setup_ui()

    def _load_icons(self):
        """加载图标"""
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icons"
        self.icons = {
            'new_folder': QIcon(str(icon_path / "new_folder.svg")),
            'copy': QIcon(str(icon_path / "copy.svg")),
            'paste': QIcon(str(icon_path / "paste.svg")),
            'cut': QIcon(str(icon_path / "cut.svg")),
            'delete': QIcon(str(icon_path / "delete.svg")),
            'rename': QIcon(str(icon_path / "rename.svg")),
            'refresh': QIcon(str(icon_path / "refresh.svg")),
            'up': QIcon(str(icon_path / "up.svg")),
            'back': QIcon(str(icon_path / "back.svg")),
            'forward': QIcon(str(icon_path / "forward.svg")),
            'search': QIcon(str(icon_path / "search.svg")),
            'filter': QIcon(str(icon_path / "filter.svg")),
            'view_list': QIcon(str(icon_path / "view_list.svg")),
            'view_detail': QIcon(str(icon_path / "view_detail.svg")),
            'view_icon': QIcon(str(icon_path / "view_icon.svg"))
        }

    def _setup_ui(self):
        """设置界面"""
        self.setMovable(False)
        self.setFloatable(False)
        self.setIconSize(QSize(24, 24))
        self._setup_navigation_actions()
        self._setup_file_actions()
        self._setup_edit_actions()
        self._setup_view_actions()

    def _setup_navigation_actions(self):
        """设置导航操作"""
        self.addSeparator()

        back_action = QAction(self)
        back_action.setIcon(self.icons['back'])
        back_action.setToolTip("后退")
        back_action.triggered.connect(self.signals.back.emit)
        self.addAction(back_action)

        forward_action = QAction(self)
        forward_action.setIcon(self.icons['forward'])
        forward_action.setToolTip("前进")
        forward_action.triggered.connect(self.signals.forward.emit)
        self.addAction(forward_action)

        up_action = QAction(self)
        up_action.setIcon(self.icons['up'])
        up_action.setToolTip("上一级")
        up_action.triggered.connect(self.signals.up.emit)
        self.addAction(up_action)

        self.addSeparator()

    def _setup_file_actions(self):
        """设置文件操作"""
        new_folder_action = QAction(self)
        new_folder_action.setIcon(self.icons['new_folder'])
        new_folder_action.setToolTip("新建文件夹")
        new_folder_action.triggered.connect(self.signals.new_folder.emit)
        self.addAction(new_folder_action)

        self.addSeparator()

    def _setup_edit_actions(self):
        """设置编辑操作"""
        copy_action = QAction(self)
        copy_action.setIcon(self.icons['copy'])
        copy_action.setToolTip("复制")
        copy_action.triggered.connect(self.signals.copy.emit)
        self.addAction(copy_action)

        paste_action = QAction(self)
        paste_action.setIcon(self.icons['paste'])
        paste_action.setToolTip("粘贴")
        paste_action.triggered.connect(self.signals.paste.emit)
        self.addAction(paste_action)

        cut_action = QAction(self)
        cut_action.setIcon(self.icons['cut'])
        cut_action.setToolTip("剪切")
        cut_action.triggered.connect(self.signals.cut.emit)
        self.addAction(cut_action)

        delete_action = QAction(self)
        delete_action.setIcon(self.icons['delete'])
        delete_action.setToolTip("删除")
        delete_action.triggered.connect(self.signals.delete.emit)
        self.addAction(delete_action)

        rename_action = QAction(self)
        rename_action.setIcon(self.icons['rename'])
        rename_action.setToolTip("重命名")
        rename_action.triggered.connect(self.signals.rename.emit)
        self.addAction(rename_action)

        self.addSeparator()

    def _setup_view_actions(self):
        """设置视图操作"""
        refresh_action = QAction(self)
        refresh_action.setIcon(self.icons['refresh'])
        refresh_action.setToolTip("刷新")
        refresh_action.triggered.connect(self.signals.refresh.emit)
        self.addAction(refresh_action)

        self.addSeparator()

        search_action = QAction(self)
        search_action.setIcon(self.icons['search'])
        search_action.setToolTip("搜索")
        search_action.triggered.connect(self.signals.search.emit)
        self.addAction(search_action)

        filter_action = QAction(self)
        filter_action.setIcon(self.icons['filter'])
        filter_action.setToolTip("过滤")
        filter_action.triggered.connect(self.signals.filter.emit)
        self.addAction(filter_action)

        self.addSeparator()

        view_list_action = QAction(self)
        view_list_action.setIcon(self.icons['view_list'])
        view_list_action.setToolTip("列表视图")
        view_list_action.triggered.connect(self.signals.view_list.emit)
        self.addAction(view_list_action)

        view_detail_action = QAction(self)
        view_detail_action.setIcon(self.icons['view_detail'])
        view_detail_action.setToolTip("详细信息视图")
        view_detail_action.triggered.connect(self.signals.view_detail.emit)
        self.addAction(view_detail_action)

        view_icon_action = QAction(self)
        view_icon_action.setIcon(self.icons['view_icon'])
        view_icon_action.setToolTip("图标视图")
        view_icon_action.triggered.connect(self.signals.view_icon.emit)
        self.addAction(view_icon_action)

    def set_action_enabled(self, action_name: str, enabled: bool):
        """
        设置操作启用状态

        Args:
            action_name: 操作名称
            enabled: 是否启用
        """
        for action in self.actions():
            if hasattr(action, 'toolTip') and action_name in action.toolTip():
                action.setEnabled(enabled)
                break
