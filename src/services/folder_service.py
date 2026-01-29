import os
import shutil
from pathlib import Path
from typing import List
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from exceptions import FileExists, FilePermissionDenied, NotADirectory
from validators.folder_validator import FolderValidator
from models.file_item import FileItem


class FolderService:
    """文件夹操作服务"""

    def __init__(self):
        """初始化文件夹服务"""
        self.validator = FolderValidator()

    def create_folder(self, folder_path: str) -> bool:
        """
        创建文件夹

        Args:
            folder_path: 文件夹路径

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(folder_path)
            self.validator.validate_folder_name(os.path.basename(folder_path))

            if os.path.exists(folder_path):
                raise FileExists(folder_path)

            os.makedirs(folder_path, exist_ok=True)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"创建文件夹失败: {str(e)}")

    def list_folders(self, folder_path: str) -> List[str]:
        """
        列出文件夹

        Args:
            folder_path: 文件夹路径

        Returns:
            文件夹列表
        """
        try:
            self.validator.validate_path(folder_path)
            self.validator.validate_folder_exists(folder_path)

            folders = []
            for entry in os.listdir(folder_path):
                entry_path = os.path.join(folder_path, entry)
                if os.path.isdir(entry_path):
                    folders.append(entry)
            return folders
        except Exception as e:
            raise NotADirectory(f"列出文件夹失败: {str(e)}")

    def delete_folder(self, folder_path: str, use_recycle_bin: bool = True, recursive: bool = False) -> bool:
        """
        删除文件夹

        Args:
            folder_path: 文件夹路径
            use_recycle_bin: 是否使用回收站
            recursive: 是否递归删除

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(folder_path)
            self.validator.validate_folder_exists(folder_path)

            if not recursive:
                self.validator.validate_folder_empty(folder_path)

            if use_recycle_bin:
                import send2trash
                send2trash.send2trash(folder_path)
            else:
                if recursive:
                    shutil.rmtree(folder_path)
                else:
                    os.rmdir(folder_path)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"删除文件夹失败: {str(e)}")

    def rename_folder(self, old_path: str, new_path: str, overwrite: bool = False) -> bool:
        """
        重命名文件夹

        Args:
            old_path: 原文件夹路径
            new_path: 新文件夹路径
            overwrite: 是否覆盖已存在的文件夹

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(old_path)
            self.validator.validate_path(new_path)
            self.validator.validate_folder_exists(old_path)
            self.validator.validate_folder_name(os.path.basename(new_path))

            if os.path.exists(new_path) and not overwrite:
                raise FileExists(new_path)

            os.rename(old_path, new_path)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"重命名文件夹失败: {str(e)}")

    def move_folder(self, src_path: str, dst_path: str, overwrite: bool = False) -> bool:
        """
        移动文件夹

        Args:
            src_path: 源文件夹路径
            dst_path: 目标文件夹路径
            overwrite: 是否覆盖已存在的文件夹

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(src_path)
            self.validator.validate_path(dst_path)
            self.validator.validate_folder_exists(src_path)

            if os.path.exists(dst_path) and not overwrite:
                raise FileExists(dst_path)

            shutil.move(src_path, dst_path)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"移动文件夹失败: {str(e)}")

    def copy_folder(self, src_path: str, dst_path: str, overwrite: bool = False) -> bool:
        """
        复制文件夹

        Args:
            src_path: 源文件夹路径
            dst_path: 目标文件夹路径
            overwrite: 是否覆盖已存在的文件夹

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(src_path)
            self.validator.validate_path(dst_path)
            self.validator.validate_folder_exists(src_path)

            if os.path.exists(dst_path) and not overwrite:
                raise FileExists(dst_path)

            shutil.copytree(src_path, dst_path, dirs_exist_ok=overwrite)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"复制文件夹失败: {str(e)}")

    def get_folder_size(self, folder_path: str) -> int:
        """
        获取文件夹大小

        Args:
            folder_path: 文件夹路径

        Returns:
            文件夹大小（字节）
        """
        try:
            self.validator.validate_path(folder_path)
            self.validator.validate_folder_exists(folder_path)

            total_size = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
            return total_size
        except Exception as e:
            raise FilePermissionDenied(f"获取文件夹大小失败: {str(e)}")

    def get_folder_info(self, folder_path: str) -> dict:
        """
        获取文件夹信息

        Args:
            folder_path: 文件夹路径

        Returns:
            文件夹信息字典
        """
        try:
            self.validator.validate_path(folder_path)
            self.validator.validate_folder_exists(folder_path)

            stat = os.stat(folder_path)
            file_count = sum(1 for _ in os.listdir(folder_path))

            return {
                'path': folder_path,
                'name': os.path.basename(folder_path),
                'size': self.get_folder_size(folder_path),
                'file_count': file_count,
                'modified_time': stat.st_mtime,
                'created_time': stat.st_ctime
            }
        except Exception as e:
            raise NotADirectory(f"获取文件夹信息失败: {str(e)}")