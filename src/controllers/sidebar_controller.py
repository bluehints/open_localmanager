from PySide6.QtCore import QObject, Signal
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from services.tree_service import TreeService


class SidebarController(QObject):
    """
    侧边栏控制器
    处理侧边栏的业务逻辑
    """

    def __init__(self, sidebar_widget, tree_service: TreeService):
        """
        初始化控制器

        Args:
            sidebar_widget: 侧边栏组件
            tree_service: 树形结构服务
        """
        super().__init__()
        self.sidebar_widget = sidebar_widget
        self.tree_service = tree_service
        self._setup_connections()

    def _setup_connections(self):
        """建立信号槽连接"""
        self.sidebar_widget.signals.node_expanded.connect(self._on_node_expanded)
        self.sidebar_widget.signals.node_collapsed.connect(self._on_node_collapsed)
        self.sidebar_widget.signals.node_selected.connect(self._on_node_selected)
        self.sidebar_widget.signals.context_menu_requested.connect(self._on_context_menu_requested)
        self.sidebar_widget.signals.context_menu_action.connect(self._on_context_menu_action)

    def _on_node_expanded(self, path: str):
        """
        处理节点展开事件

        Args:
            path: 节点路径
        """
        try:
            self.tree_service.load_children(path)
        except Exception as e:
            pass

    def _on_node_collapsed(self, path: str):
        """
        处理节点收起事件

        Args:
            path: 节点路径
        """
        pass

    def _on_node_selected(self, path: str):
        """
        处理节点选择事件

        Args:
            path: 节点路径
        """
        try:
            self.tree_service.select_node(path)
        except Exception as e:
            pass

    def _on_context_menu_requested(self, path: str, position):
        """
        处理右键菜单请求事件

        Args:
            path: 节点路径
            position: 位置
        """
        pass

    def _on_context_menu_action(self, action_type: str, path: str):
        """
        处理右键菜单动作事件

        Args:
            action_type: 动作类型
            path: 路径
        """
        if action_type == "open":
            self.sidebar_widget.signals.node_selected.emit(path)
        elif action_type == "expand":
            self._expand_node(path)
        elif action_type == "collapse":
            self._collapse_node(path)
        elif action_type == "refresh":
            self._refresh_node(path)

    def _expand_node(self, path: str):
        """
        展开节点

        Args:
            path: 路径
        """
        items = self.sidebar_widget.tree_widget.findItems(
            path, Qt.MatchExactly | Qt.MatchRecursive, 0
        )
        if items:
            item = items[0]
            item.setExpanded(True)

    def _collapse_node(self, path: str):
        """
        收起节点

        Args:
            path: 路径
        """
        items = self.sidebar_widget.tree_widget.findItems(
            path, Qt.MatchExactly | Qt.MatchRecursive, 0
        )
        if items:
            item = items[0]
            item.setExpanded(False)

    def _refresh_node(self, path: str):
        """
        刷新节点

        Args:
            path: 路径
        """
        items = self.sidebar_widget.tree_widget.findItems(
            path, Qt.MatchExactly | Qt.MatchRecursive, 0
        )
        if items:
            item = items[0]
            item.setExpanded(False)
            item.setExpanded(True)

    def sync_with_file_manager(self, file_path: str):
        """
        与文件管理区同步

        Args:
            file_path: 文件路径
        """
        pass
