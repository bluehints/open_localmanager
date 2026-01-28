import os
import re
from pathlib import Path
from typing import List
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from exceptions import FileNotFound, FilePermissionDenied, InvalidPath


class FileValidator:
    """文件验证器"""

    INVALID_CHARS = r'[<>:"|?*]'
    INVALID_NAMES = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']

    @staticmethod
    def validate_path(path: str) -> bool:
        """
        验证路径是否有效

        Args:
            path: 文件路径

        Returns:
            是否有效
        """
        if not path or not isinstance(path, str):
            return False

        try:
            Path(path)
            return True
        except Exception:
            return False

    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """
        验证文件是否存在

        Args:
            file_path: 文件路径

        Returns:
            是否存在

        Raises:
            FileNotFound: 文件不存在
        """
        if not os.path.exists(file_path):
            raise FileNotFound(file_path)
        if not os.path.isfile(file_path):
            raise FileNotFound(file_path)
        return True

    @staticmethod
    def validate_file_permission(file_path: str) -> bool:
        """
        验证文件权限

        Args:
            file_path: 文件路径

        Returns:
            是否有权限

        Raises:
            FilePermissionDenied: 权限不足
        """
        if not os.access(file_path, os.R_OK):
            raise FilePermissionDenied(file_path)
        return True

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        验证文件名是否有效

        Args:
            name: 文件名

        Returns:
            是否有效
        """
        return FileValidator.validate_filename(name)

    @staticmethod
    def validate_filename(filename: str) -> bool:
        """
        验证文件名是否有效

        Args:
            filename: 文件名

        Returns:
            是否有效

        Raises:
            InvalidPath: 文件名无效
        """
        if not filename:
            raise InvalidPath(filename)

        name_without_ext = os.path.splitext(filename)[0].upper()

        if name_without_ext in FileValidator.INVALID_NAMES:
            raise InvalidPath(f"文件名无效: {filename}")

        if re.search(FileValidator.INVALID_CHARS, filename):
            raise InvalidPath(f"文件名包含无效字符: {filename}")

        if len(filename) > 255:
            raise InvalidPath(f"文件名过长: {filename}")

        return True

    @staticmethod
    def validate_file_size(file_path: str, max_size: int = 1024 * 1024 * 1024) -> bool:
        """
        验证文件大小

        Args:
            file_path: 文件路径
            max_size: 最大大小（字节）

        Returns:
            是否在限制内

        Raises:
            FilePermissionDenied: 文件过大
        """
        if not os.path.exists(file_path):
            raise FileNotFound(file_path)

        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            raise FilePermissionDenied(f"文件过大: {file_path}")

        return True

    @staticmethod
    def validate_extension(file_path: str, allowed_extensions: List[str]) -> bool:
        """
        验证文件扩展名

        Args:
            file_path: 文件路径
            allowed_extensions: 允许的扩展名列表

        Returns:
            是否在允许列表中

        Raises:
            InvalidPath: 扩展名不允许
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext not in [e.lower() for e in allowed_extensions]:
            raise InvalidPath(f"文件扩展名不允许: {ext}")

        return True