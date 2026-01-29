from PySide6.QtWidgets import QToolBar, QStyle
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject, Signal, QSize


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
        self._setup_ui()

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
        back_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
        back_action.setToolTip("后退")
        back_action.triggered.connect(self.signals.back.emit)
        self.addAction(back_action)

        forward_action = QAction(self)
        forward_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        forward_action.setToolTip("前进")
        forward_action.triggered.connect(self.signals.forward.emit)
        self.addAction(forward_action)

        up_action = QAction(self)
        up_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))
        up_action.setToolTip("上一级")
        up_action.triggered.connect(self.signals.up.emit)
        self.addAction(up_action)

        self.addSeparator()

    def _setup_file_actions(self):
        """设置文件操作"""
        new_folder_action = QAction(self)
        new_folder_action.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        new_folder_action.setToolTip("新建文件夹")
        new_folder_action.triggered.connect(self.signals.new_folder.emit)
        self.addAction(new_folder_action)

        self.addSeparator()

    def _setup_edit_actions(self):
        """设置编辑操作"""
        copy_action = QAction(self)
        copy_action.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        copy_action.setToolTip("复制")
        copy_action.triggered.connect(self.signals.copy.emit)
        self.addAction(copy_action)

        paste_action = QAction(self)
        paste_action.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        paste_action.setToolTip("粘贴")
        paste_action.triggered.connect(self.signals.paste.emit)
        self.addAction(paste_action)

        cut_action = QAction(self)
        cut_action.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        cut_action.setToolTip("剪切")
        cut_action.triggered.connect(self.signals.cut.emit)
        self.addAction(cut_action)

        delete_action = QAction(self)
        delete_action.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        delete_action.setToolTip("删除")
        delete_action.triggered.connect(self.signals.delete.emit)
        self.addAction(delete_action)

        rename_action = QAction(self)
        rename_action.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        rename_action.setToolTip("重命名")
        rename_action.triggered.connect(self.signals.rename.emit)
        self.addAction(rename_action)

        self.addSeparator()

    def _setup_view_actions(self):
        """设置视图操作"""
        refresh_action = QAction(self)
        refresh_action.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        refresh_action.setToolTip("刷新")
        refresh_action.triggered.connect(self.signals.refresh.emit)
        self.addAction(refresh_action)

        view_list_action = QAction(self)
        view_list_action.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        view_list_action.setToolTip("列表视图")
        view_list_action.triggered.connect(self.signals.view_list.emit)
        self.addAction(view_list_action)

        view_detail_action = QAction(self)
        view_detail_action.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        view_detail_action.setToolTip("详细信息视图")
        view_detail_action.triggered.connect(self.signals.view_detail.emit)
        self.addAction(view_detail_action)

        view_icon_action = QAction(self)
        view_icon_action.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
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