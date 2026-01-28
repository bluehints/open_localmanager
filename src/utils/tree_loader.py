import os
from typing import List, Optional
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.tree_item import TreeItem


class TreeLoader:
    """
    树形结构加载器
    负责加载文件系统的树形结构
    """

    def __init__(self):
        """初始化加载器"""
        self._hidden_files = False

    def set_show_hidden(self, show: bool):
        """
        设置是否显示隐藏文件

        Args:
            show: 是否显示
        """
        self._hidden_files = show

    def load_tree(self, root_path: str) -> Optional[TreeItem]:
        """
        加载树形结构

        Args:
            root_path: 根路径

        Returns:
            树形结构根节点
        """
        if not os.path.exists(root_path):
            return None

        if not os.path.isdir(root_path):
            return None

        root_item = TreeItem(
            path=root_path,
            name=os.path.basename(root_path),
            is_folder=True
        )

        self._load_children(root_item, root_path)

        return root_item

    def _load_children(self, parent_item: TreeItem, parent_path: str):
        """
        加载子节点

        Args:
            parent_item: 父节点
            parent_path: 父路径
        """
        try:
            entries = os.listdir(parent_path)
            entries.sort()

            for entry in entries:
                if not self._hidden_files and entry.startswith('.'):
                    continue

                entry_path = os.path.join(parent_path, entry)

                if os.path.isdir(entry_path):
                    child_item = TreeItem(
                        path=entry_path,
                        name=entry,
                        is_folder=True,
                        parent=parent_item
                    )
                    parent_item.add_child(child_item)

        except Exception:
            pass

    def load_children(self, path: str) -> List[TreeItem]:
        """
        加载指定路径的子节点

        Args:
            path: 路径

        Returns:
            子节点列表
        """
        children = []

        if not os.path.exists(path):
            return children

        if not os.path.isdir(path):
            return children

        try:
            entries = os.listdir(path)
            entries.sort()

            for entry in entries:
                if not self._hidden_files and entry.startswith('.'):
                    continue

                entry_path = os.path.join(path, entry)

                if os.path.isdir(entry_path):
                    child_item = TreeItem(
                        path=entry_path,
                        name=entry,
                        is_folder=True
                    )
                    children.append(child_item)

        except Exception:
            pass

        return children

    def has_children(self, path: str) -> bool:
        """
        判断路径是否有子目录

        Args:
            path: 路径

        Returns:
            是否有子目录
        """
        if not os.path.exists(path):
            return False

        if not os.path.isdir(path):
            return False

        try:
            entries = os.listdir(path)
            for entry in entries:
                if not self._hidden_files and entry.startswith('.'):
                    continue

                entry_path = os.path.join(path, entry)
                if os.path.isdir(entry_path):
                    return True

        except Exception:
            pass

        return False