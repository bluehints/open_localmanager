from enum import Enum
from typing import List
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.file_item import FileItem


class FilterType(Enum):
    """过滤类型枚举"""
    ALL = 0
    FILES_ONLY = 1
    FOLDERS_ONLY = 2


class FileFilter:
    """
    文件过滤工具
    提供文件过滤功能
    """

    def __init__(self):
        """初始化过滤器"""
        self._filter_type = FilterType.ALL
        self._filter_text = ""
        self._show_hidden = False
        self._extension_filter = ""

    def set_filter_type(self, filter_type: FilterType):
        """
        设置过滤类型

        Args:
            filter_type: 过滤类型
        """
        self._filter_type = filter_type

    def set_filter_text(self, text: str):
        """
        设置过滤文本

        Args:
            text: 过滤文本
        """
        self._filter_text = text.lower()

    def set_show_hidden(self, show: bool):
        """
        设置是否显示隐藏文件

        Args:
            show: 是否显示
        """
        self._show_hidden = show

    def set_extension_filter(self, extension: str):
        """
        设置扩展名过滤

        Args:
            extension: 扩展名
        """
        self._extension_filter = extension.lower()

    def filter(self, files: List[FileItem]) -> List[FileItem]:
        """
        过滤文件列表

        Args:
            files: 文件列表

        Returns:
            过滤后的文件列表
        """
        filtered_files = files

        filtered_files = self._filter_by_type(filtered_files)
        filtered_files = self._filter_by_text(filtered_files)
        filtered_files = self._filter_by_hidden(filtered_files)
        filtered_files = self._filter_by_extension(filtered_files)

        return filtered_files

    def _filter_by_type(self, files: List[FileItem]) -> List[FileItem]:
        """
        按类型过滤

        Args:
            files: 文件列表

        Returns:
            过滤后的文件列表
        """
        if self._filter_type == FilterType.ALL:
            return files
        elif self._filter_type == FilterType.FILES_ONLY:
            return [f for f in files if not f.is_folder]
        elif self._filter_type == FilterType.FOLDERS_ONLY:
            return [f for f in files if f.is_folder]
        else:
            return files

    def _filter_by_text(self, files: List[FileItem]) -> List[FileItem]:
        """
        按文本过滤

        Args:
            files: 文件列表

        Returns:
            过滤后的文件列表
        """
        if not self._filter_text:
            return files

        return [f for f in files if self._filter_text in f.name.lower()]

    def _filter_by_hidden(self, files: List[FileItem]) -> List[FileItem]:
        """
        按隐藏文件过滤

        Args:
            files: 文件列表

        Returns:
            过滤后的文件列表
        """
        if self._show_hidden:
            return files

        return [f for f in files if not os.path.basename(f.path).startswith('.')]

    def _filter_by_extension(self, files: List[FileItem]) -> List[FileItem]:
        """
        按扩展名过滤

        Args:
            files: 文件列表

        Returns:
            过滤后的文件列表
        """
        if not self._extension_filter:
            return files

        return [f for f in files if f.name.lower().endswith(self._extension_filter)]

    def get_filter_type(self) -> FilterType:
        """
        获取过滤类型

        Returns:
            过滤类型
        """
        return self._filter_type

    def get_filter_text(self) -> str:
        """
        获取过滤文本

        Returns:
            过滤文本
        """
        return self._filter_text

    def is_show_hidden(self) -> bool:
        """
        获取是否显示隐藏文件

        Returns:
            是否显示
        """
        return self._show_hidden

    def get_extension_filter(self) -> str:
        """
        获取扩展名过滤

        Returns:
            扩展名
        """
        return self._extension_filter