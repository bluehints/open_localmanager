from PySide6.QtCore import QSortFilterProxyModel, Qt, QModelIndex
from typing import Optional
from models.file_item import FileItem


class FileSortFilterProxyModel(QSortFilterProxyModel):
    """文件排序过滤模型"""

    def __init__(self, parent=None):
        """
        初始化文件排序过滤模型

        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self._filter_text = ""
        self._show_hidden = False
        self._filter_folders = False
        self._filter_files = False

    def set_filter_text(self, text: str):
        """
        设置过滤文本

        Args:
            text: 过滤文本
        """
        self._filter_text = text.lower()
        self.invalidateFilter()

    def set_show_hidden(self, show: bool):
        """
        设置是否显示隐藏文件

        Args:
            show: 是否显示
        """
        self._show_hidden = show
        self.invalidateFilter()

    def set_filter_folders(self, filter_folders: bool):
        """
        设置是否过滤文件夹

        Args:
            filter_folders: 是否过滤文件夹
        """
        self._filter_folders = filter_folders
        self.invalidateFilter()

    def set_filter_files(self, filter_files: bool):
        """
        设置是否过滤文件

        Args:
            filter_files: 是否过滤文件
        """
        self._filter_files = filter_files
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        过滤行

        Args:
            source_row: 源行号
            source_parent: 源父索引

        Returns:
            是否接受该行
        """
        source_model = self.sourceModel()
        if not source_model:
            return False

        index = source_model.index(source_row, 0, source_parent)
        if not index.isValid():
            return False

        file_item = source_model.get_file(index)
        if not file_item:
            return False

        if not self._show_hidden and file_item.name.startswith('.'):
            return False

        if self._filter_folders and file_item.is_folder:
            return False

        if self._filter_files and not file_item.is_folder:
            return False

        if self._filter_text:
            if self._filter_text not in file_item.name.lower():
                return False

        return True

    def lessThan(self, source_left: QModelIndex, source_right: QModelIndex) -> bool:
        """
        比较两个索引

        Args:
            source_left: 左侧索引
            source_right: 右侧索引

        Returns:
            左侧是否小于右侧
        """
        source_model = self.sourceModel()
        if not source_model:
            return False

        left_item = source_model.get_file(source_left)
        right_item = source_model.get_file(source_right)

        if not left_item or not right_item:
            return False

        sort_column = self.sortColumn()
        sort_order = self.sortOrder()

        if sort_column == 0:
            left_name = left_item.name.lower()
            right_name = right_item.name.lower()
            if sort_order == Qt.AscendingOrder:
                return left_name < right_name
            else:
                return left_name > right_name

        elif sort_column == 1:
            if sort_order == Qt.AscendingOrder:
                return left_item.size < right_item.size
            else:
                return left_item.size > right_item.size

        elif sort_column == 2:
            if sort_order == Qt.AscendingOrder:
                return left_item.modified_time < right_item.modified_time
            else:
                return left_item.modified_time > right_item.modified_time

        elif sort_column == 3:
            left_type = left_item.file_type.lower()
            right_type = right_item.file_type.lower()
            if sort_order == Qt.AscendingOrder:
                return left_type < right_type
            else:
                return left_type > right_type

        return False