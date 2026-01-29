from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from typing import Any, List
from .file_item import FileItem


class FileTableModel(QAbstractTableModel):
    """文件表格模型"""

    def __init__(self, files: List[FileItem] = None, parent=None):
        """
        初始化文件表格模型

        Args:
            files: 文件列表
            parent: 父对象
        """
        super().__init__(parent)
        self._files = files if files is not None else []
        self._headers = ["名称", "大小", "修改时间", "类型"]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        获取行数

        Args:
            parent: 父索引

        Returns:
            行数
        """
        return len(self._files)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        获取列数

        Args:
            parent: 父索引

        Returns:
            列数
        """
        return len(self._headers)

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

        if index.row() >= len(self._files):
            return None

        file_item = self._files[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:
                return file_item.name
            elif column == 1:
                return file_item.get_size_str()
            elif column == 2:
                return file_item.get_modified_time_str()
            elif column == 3:
                return file_item.file_type

        if role == Qt.TextAlignmentRole:
            if column == 1:
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        """
        获取表头数据

        Args:
            section: 节
            orientation: 方向
            role: 角色

        Returns:
            表头数据
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None

    def refresh(self, files: List[FileItem]) -> None:
        """
        刷新模型

        Args:
            files: 文件列表
        """
        self.beginResetModel()
        self._files = files
        self.endResetModel()

    def get_file(self, index: QModelIndex) -> FileItem:
        """
        获取文件项

        Args:
            index: 索引

        Returns:
            文件项
        """
        if not index.isValid():
            return None
        return self._files[index.row()]