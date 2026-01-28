import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from exceptions import NotADirectory, DirectoryNotEmpty, InvalidPath


class FolderValidator:
    """文件夹验证器"""

    INVALID_CHARS = r'[<>:"|?*]'
    INVALID_NAMES = ['CON', 'PRN', 'AUX', 'NUL']

    @staticmethod
    def validate_path(path: str) -> bool:
        """
        验证路径是否有效

        Args:
            path: 文件夹路径

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
    def validate_folder_exists(folder_path: str) -> bool:
        """
        验证文件夹是否存在

        Args:
            folder_path: 文件夹路径

        Returns:
            是否存在

        Raises:
            NotADirectory: 不是文件夹
        """
        if not os.path.exists(folder_path):
            raise NotADirectory(folder_path)
        if not os.path.isdir(folder_path):
            raise NotADirectory(folder_path)
        return True

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        验证文件夹名是否有效

        Args:
            name: 文件夹名

        Returns:
            是否有效
        """
        return FolderValidator.validate_folder_name(name)

    @staticmethod
    def validate_folder_name(folder_name: str) -> bool:
        """
        验证文件夹名是否有效

        Args:
            folder_name: 文件夹名

        Returns:
            是否有效

        Raises:
            InvalidPath: 文件夹名无效
        """
        if not folder_name:
            raise InvalidPath(folder_name)

        name_upper = folder_name.upper()

        if name_upper in FolderValidator.INVALID_NAMES:
            raise InvalidPath(f"文件夹名无效: {folder_name}")

        if any(char in folder_name for char in ['<', '>', ':', '"', '|', '?', '*']):
            raise InvalidPath(f"文件夹名包含无效字符: {folder_name}")

        if len(folder_name) > 255:
            raise InvalidPath(f"文件夹名过长: {folder_name}")

        return True

    @staticmethod
    def validate_folder_empty(folder_path: str) -> bool:
        """
        验证文件夹是否为空

        Args:
            folder_path: 文件夹路径

        Returns:
            是否为空

        Raises:
            DirectoryNotEmpty: 文件夹不为空
        """
        if not os.path.exists(folder_path):
            raise NotADirectory(folder_path)

        items = os.listdir(folder_path)
        if items:
            raise DirectoryNotEmpty(folder_path)
        return True