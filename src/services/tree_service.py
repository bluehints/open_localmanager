import os
import sys
from pathlib import Path
from typing import List, Optional
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.tree_item import TreeItem
from utils.tree_loader import TreeLoader


class TreeService:
    """
    树形结构服务
    提供树形结构的业务逻辑
    """

    def __init__(self):
        """初始化服务"""
        self.loader = TreeLoader()
        self._root_item: Optional[TreeItem] = None
        self._selected_path: Optional[str] = None

    def load_tree(self, root_path: str) -> Optional[TreeItem]:
        """
        加载树形结构

        Args:
            root_path: 根路径

        Returns:
            树形结构根节点
        """
        self._root_item = self.loader.load_tree(root_path)
        return self._root_item

    def load_children(self, path: str) -> List[TreeItem]:
        """
        加载子节点

        Args:
            path: 路径

        Returns:
            子节点列表
        """
        return self.loader.load_children(path)

    def select_node(self, path: str) -> bool:
        """
        选中节点

        Args:
            path: 路径

        Returns:
            是否成功
        """
        if not os.path.exists(path):
            return False

        self._selected_path = path
        return True

    def get_selected_path(self) -> Optional[str]:
        """
        获取选中的路径

        Returns:
            选中路径
        """
        return self._selected_path

    def get_root_item(self) -> Optional[TreeItem]:
        """
        获取根节点

        Returns:
            根节点
        """
        return self._root_item

    def find_item(self, path: str) -> Optional[TreeItem]:
        """
        查找节点

        Args:
            path: 路径

        Returns:
            节点
        """
        if not self._root_item:
            return None

        return self._find_item_recursive(self._root_item, path)

    def _find_item_recursive(self, item: TreeItem, path: str) -> Optional[TreeItem]:
        """
        递归查找节点

        Args:
            item: 当前节点
            path: 路径

        Returns:
            节点
        """
        if item.path == path:
            return item

        for child in item.children:
            result = self._find_item_recursive(child, path)
            if result:
                return result

        return None

    def set_show_hidden(self, show: bool):
        """
        设置是否显示隐藏文件

        Args:
            show: 是否显示
        """
        self.loader.set_show_hidden(show)

    def refresh(self, path: str):
        """
        刷新节点

        Args:
            path: 路径
        """
        pass