import os
from pathlib import Path
from typing import List, Optional
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class PathHelper:
    """
    路径辅助工具
    提供路径处理功能
    """

    @staticmethod
    def normalize(path: str) -> str:
        """
        规范化路径

        Args:
            path: 路径

        Returns:
            规范化后的路径
        """
        return os.path.normpath(path)

    @staticmethod
    def join(*paths: str) -> str:
        """
        连接路径

        Args:
            *paths: 路径段

        Returns:
            连接后的路径
        """
        return os.path.join(*paths)

    @staticmethod
    def split(path: str) -> tuple:
        """
        分割路径

        Args:
            path: 路径

        Returns:
            (目录, 文件名)
        """
        return os.path.split(path)

    @staticmethod
    def get_basename(path: str) -> str:
        """
        获取文件名

        Args:
            path: 路径

        Returns:
            文件名
        """
        return os.path.basename(path)

    @staticmethod
    def get_dirname(path: str) -> str:
        """
        获取目录名

        Args:
            path: 路径

        Returns:
            目录名
        """
        return os.path.dirname(path)

    @staticmethod
    def get_extension(path: str) -> str:
        """
        获取文件扩展名

        Args:
            path: 路径

        Returns:
            扩展名
        """
        return os.path.splitext(path)[1].lower()

    @staticmethod
    def get_filename_without_extension(path: str) -> str:
        """
        获取不带扩展名的文件名

        Args:
            path: 路径

        Returns:
            不带扩展名的文件名
        """
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def is_absolute(path: str) -> bool:
        """
        判断是否为绝对路径

        Args:
            path: 路径

        Returns:
            是否为绝对路径
        """
        return os.path.isabs(path)

    @staticmethod
    def make_absolute(path: str, base: Optional[str] = None) -> str:
        """
        转换为绝对路径

        Args:
            path: 路径
            base: 基础路径

        Returns:
            绝对路径
        """
        if PathHelper.is_absolute(path):
            return path
        if base:
            return os.path.abspath(os.path.join(base, path))
        return os.path.abspath(path)

    @staticmethod
    def is_subpath(parent: str, child: str) -> bool:
        """
        判断是否为子路径

        Args:
            parent: 父路径
            child: 子路径

        Returns:
            是否为子路径
        """
        parent = PathHelper.normalize(parent)
        child = PathHelper.normalize(child)
        return child.startswith(parent)

    @staticmethod
    def get_relative_path(path: str, base: str) -> str:
        """
        获取相对路径

        Args:
            path: 路径
            base: 基础路径

        Returns:
            相对路径
        """
        try:
            return os.path.relpath(path, base)
        except Exception:
            return path

    @staticmethod
    def exists(path: str) -> bool:
        """
        判断路径是否存在

        Args:
            path: 路径

        Returns:
            是否存在
        """
        return os.path.exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        """
        判断是否为文件

        Args:
            path: 路径

        Returns:
            是否为文件
        """
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        """
        判断是否为目录

        Args:
            path: 路径

        Returns:
            是否为目录
        """
        return os.path.isdir(path)

    @staticmethod
    def get_size(path: str) -> int:
        """
        获取路径大小

        Args:
            path: 路径

        Returns:
            大小（字节）
        """
        if PathHelper.is_file(path):
            return os.path.getsize(path)
        elif PathHelper.is_dir(path):
            total_size = 0
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except Exception:
                        pass
            return total_size
        return 0

    @staticmethod
    def split_all(path: str) -> List[str]:
        """
        分割所有路径部分

        Args:
            path: 路径

        Returns:
            路径部分列表
        """
        parts = []
        while True:
            path, part = os.path.split(path)
            if part:
                parts.insert(0, part)
            else:
                if path:
                    parts.insert(0, path)
                break
        return parts

    @staticmethod
    def get_common_path(paths: List[str]) -> str:
        """
        获取公共路径

        Args:
            paths: 路径列表

        Returns:
            公共路径
        """
        if not paths:
            return ""
        return os.path.commonpath(paths)