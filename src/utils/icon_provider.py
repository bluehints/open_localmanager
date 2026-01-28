import os
from pathlib import Path
from typing import Optional
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QFileIconProvider


class IconProvider:
    """图标提供器"""

    def __init__(self):
        """初始化图标提供器"""
        self.icon_provider = QFileIconProvider()
        self._icon_cache = {}

    def get_icon(self, file_path: str) -> QIcon:
        """
        获取文件图标

        Args:
            file_path: 文件路径

        Returns:
            文件图标
        """
        if file_path in self._icon_cache:
            return self._icon_cache[file_path]

        file_info = QFileInfo(file_path)
        icon = self.icon_provider.icon(file_info)
        self._icon_cache[file_path] = icon
        return icon

    def get_folder_icon(self) -> QIcon:
        """
        获取文件夹图标

        Returns:
            文件夹图标
        """
        if 'folder' in self._icon_cache:
            return self._icon_cache['folder']

        icon = self.icon_provider.icon(QFileIconProvider.Folder)
        self._icon_cache['folder'] = icon
        return icon

    def get_file_icon(self, extension: str) -> QIcon:
        """
        根据扩展名获取文件图标

        Args:
            extension: 文件扩展名

        Returns:
            文件图标
        """
        cache_key = f'file_{extension}'
        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]

        icon = self.icon_provider.icon(QFileInfo(f'file{extension}'))
        self._icon_cache[cache_key] = icon
        return icon

    def get_icon_for_type(self, file_type: str) -> QIcon:
        """
        根据文件类型获取图标

        Args:
            file_type: 文件类型

        Returns:
            文件图标
        """
        if file_type == 'folder':
            return self.get_folder_icon()
        elif file_type == 'file':
            return self.get_file_icon('.txt')
        else:
            return self.get_file_icon('.txt')

    def clear_cache(self) -> None:
        """清空图标缓存"""
        self._icon_cache.clear()

    def get_icon_size(self) -> int:
        """
        获取图标大小

        Returns:
            图标大小（像素）
        """
        return 32