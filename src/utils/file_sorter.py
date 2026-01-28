from enum import Enum
from typing import List
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.file_item import FileItem


class SortColumn(Enum):
    """排序列枚举"""
    NAME = 0
    SIZE = 1
    TYPE = 2
    MODIFIED_TIME = 3


class SortOrder(Enum):
    """排序顺序枚举"""
    ASCENDING = 0
    DESCENDING = 1


class FileSorter:
    """
    文件排序工具
    提供文件排序功能
    """

    def __init__(self):
        """初始化排序器"""
        self._sort_column = SortColumn.NAME
        self._sort_order = SortOrder.ASCENDING

    def set_sort_column(self, column: SortColumn):
        """
        设置排序列

        Args:
            column: 排序列
        """
        self._sort_column = column

    def set_sort_order(self, order: SortOrder):
        """
        设置排序顺序

        Args:
            order: 排序顺序
        """
        self._sort_order = order

    def sort(self, files: List[FileItem]) -> List[FileItem]:
        """
        排序文件列表

        Args:
            files: 文件列表

        Returns:
            排序后的文件列表
        """
        if self._sort_column == SortColumn.NAME:
            return self._sort_by_name(files)
        elif self._sort_column == SortColumn.SIZE:
            return self._sort_by_size(files)
        elif self._sort_column == SortColumn.TYPE:
            return self._sort_by_type(files)
        elif self._sort_column == SortColumn.MODIFIED_TIME:
            return self._sort_by_modified_time(files)
        else:
            return files

    def _sort_by_name(self, files: List[FileItem]) -> List[FileItem]:
        """
        按名称排序

        Args:
            files: 文件列表

        Returns:
            排序后的文件列表
        """
        sorted_files = sorted(files, key=lambda x: x.name.lower())
        if self._sort_order == SortOrder.DESCENDING:
            sorted_files.reverse()
        return sorted_files

    def _sort_by_size(self, files: List[FileItem]) -> List[FileItem]:
        """
        按大小排序

        Args:
            files: 文件列表

        Returns:
            排序后的文件列表
        """
        sorted_files = sorted(files, key=lambda x: x.size)
        if self._sort_order == SortOrder.DESCENDING:
            sorted_files.reverse()
        return sorted_files

    def _sort_by_type(self, files: List[FileItem]) -> List[FileItem]:
        """
        按类型排序

        Args:
            files: 文件列表

        Returns:
            排序后的文件列表
        """
        sorted_files = sorted(files, key=lambda x: x.file_type.lower())
        if self._sort_order == SortOrder.DESCENDING:
            sorted_files.reverse()
        return sorted_files

    def _sort_by_modified_time(self, files: List[FileItem]) -> List[FileItem]:
        """
        按修改时间排序

        Args:
            files: 文件列表

        Returns:
            排序后的文件列表
        """
        sorted_files = sorted(files, key=lambda x: x.modified_time)
        if self._sort_order == SortOrder.DESCENDING:
            sorted_files.reverse()
        return sorted_files

    def get_sort_column(self) -> SortColumn:
        """
        获取排序列

        Returns:
            排序列
        """
        return self._sort_column

    def get_sort_order(self) -> SortOrder:
        """
        获取排序顺序

        Returns:
            排序顺序
        """
        return self._sort_order