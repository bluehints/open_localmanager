from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from typing import Any
from .tree_item import TreeItem


class TreeItemModel(QAbstractItemModel):
    """树形结构项模型"""

    def __init__(self, root_item: TreeItem, parent=None):
        """
        初始化树形结构项模型

        Args:
            root_item: 根节点
            parent: 父对象
        """
        super().__init__(parent)
        self._root_item = root_item

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        """
        获取索引

        Args:
            row: 行号
            column: 列号
            parent: 父索引

        Returns:
            索引
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.children[row] if row < len(parent_item.children) else None
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        """
        获取父索引

        Args:
            index: 索引

        Returns:
            父索引
        """
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent

        if parent_item == self._root_item or parent_item is None:
            return QModelIndex()

        return self.createIndex(parent_item.get_row(), 0, parent_item)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        获取行数

        Args:
            parent: 父索引

        Returns:
            行数
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.get_child_count()

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        获取列数

        Args:
            parent: 父索引

        Returns:
            列数
        """
        return 1

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        """
        获取数据

        Args:
            index: 索引
            role: 角色

        Returns:
            数据
        """
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            return item.name

        if role == Qt.DecorationRole:
            return None

        return None

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        """
        设置数据

        Args:
            index: 索引
            value: 值
            role: 角色

        Returns:
            是否成功
        """
        if not index.isValid():
            return False

        item = index.internalPointer()

        if role == Qt.EditRole:
            item.name = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True

        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        获取标志

        Args:
            index: 索引

        Returns:
            标志
        """
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def refresh(self):
        """刷新模型"""
        self.beginResetModel()
        self.endResetModel()