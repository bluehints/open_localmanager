from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TreeItem:
    """树形结构项，用于表示文件系统中的文件或文件夹节点"""

    path: str
    name: str
    is_folder: bool
    is_expanded: bool = False
    children: List['TreeItem'] = field(default_factory=list)
    parent: Optional['TreeItem'] = None

    def add_child(self, child: 'TreeItem') -> None:
        """
        添加子节点

        Args:
            child: 子节点
        """
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: 'TreeItem') -> None:
        """
        移除子节点

        Args:
            child: 子节点
        """
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def get_child_count(self) -> int:
        """
        获取子节点数量

        Returns:
            子节点数量
        """
        return len(self.children)

    def has_children(self) -> bool:
        """
        是否有子节点

        Returns:
            是否有子节点
        """
        return len(self.children) > 0

    def get_row(self) -> int:
        """
        获取在父节点中的行号

        Returns:
            行号
        """
        if self.parent is not None:
            return self.parent.children.index(self)
        return 0