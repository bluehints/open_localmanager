import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from exceptions import FileNotFound, FileExists, FilePermissionDenied
from validators.file_validator import FileValidator
from models.file_item import FileItem


class FileService:
    """文件操作服务"""

    def __init__(self):
        """初始化文件服务"""
        self.validator = FileValidator()

    def copy_file(self, src_path: str, dst_path: str, overwrite: bool = False) -> bool:
        """
        复制文件

        Args:
            src_path: 源文件路径
            dst_path: 目标文件路径
            overwrite: 是否覆盖已存在的文件

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(src_path)
            self.validator.validate_path(dst_path)
            self.validator.validate_file_exists(src_path)
            self.validator.validate_file_permission(src_path)

            if os.path.exists(dst_path) and not overwrite:
                raise FileExists(dst_path)

            shutil.copy2(src_path, dst_path)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"复制文件失败: {str(e)}")

    def move_file(self, src_path: str, dst_path: str, overwrite: bool = False) -> bool:
        """
        移动文件

        Args:
            src_path: 源文件路径
            dst_path: 目标文件路径
            overwrite: 是否覆盖已存在的文件

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(src_path)
            self.validator.validate_path(dst_path)
            self.validator.validate_file_exists(src_path)
            self.validator.validate_file_permission(src_path)

            if os.path.exists(dst_path) and not overwrite:
                raise FileExists(dst_path)

            shutil.move(src_path, dst_path)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"移动文件失败: {str(e)}")

    def delete_file(self, file_path: str, use_recycle_bin: bool = True) -> bool:
        """
        删除文件

        Args:
            file_path: 文件路径
            use_recycle_bin: 是否使用回收站

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(file_path)
            self.validator.validate_file_exists(file_path)
            self.validator.validate_file_permission(file_path)

            if use_recycle_bin:
                import send2trash
                send2trash.send2trash(file_path)
            else:
                os.remove(file_path)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"删除文件失败: {str(e)}")

    def rename_file(self, old_path: str, new_path: str, overwrite: bool = False) -> bool:
        """
        重命名文件

        Args:
            old_path: 旧文件路径
            new_path: 新文件路径
            overwrite: 是否覆盖已存在的文件

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(old_path)
            self.validator.validate_path(new_path)
            self.validator.validate_file_exists(old_path)
            self.validator.validate_file_permission(old_path)

            if os.path.exists(new_path) and not overwrite:
                raise FileExists(new_path)

            os.rename(old_path, new_path)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"重命名文件失败: {str(e)}")

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取文件信息

        Args:
            file_path: 文件路径

        Returns:
            文件信息字典
        """
        try:
            self.validator.validate_path(file_path)
            self.validator.validate_file_exists(file_path)

            if not os.path.exists(file_path):
                raise FileNotFound(file_path)

            stat = os.stat(file_path)
            is_folder = os.path.isdir(file_path)
            file_type = os.path.splitext(file_path)[1] if not is_folder else 'folder'

            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'modified_time': datetime.fromtimestamp(stat.st_mtime),
                'created_time': datetime.fromtimestamp(stat.st_ctime),
                'is_folder': is_folder,
                'file_type': file_type
            }
        except Exception as e:
            raise FileNotFound(f"获取文件信息失败: {str(e)}")

    def list_files(self, folder_path: str, include_hidden: bool = False) -> List[FileItem]:
        """
        列出文件夹内容

        Args:
            folder_path: 文件夹路径
            include_hidden: 是否包含隐藏文件

        Returns:
            文件列表
        """
        try:
            self.validator.validate_path(folder_path)
            
            if not os.path.exists(folder_path):
                raise FileNotFound(folder_path)
            if not os.path.isdir(folder_path):
                raise FileNotFound(folder_path)

            files = []
            for item in os.listdir(folder_path):
                if not include_hidden and item.startswith('.'):
                    continue

                item_path = os.path.join(folder_path, item)
                file_info = self.get_file_info(item_path)
                files.append(FileItem(
                    path=file_info['path'],
                    name=file_info['name'],
                    size=file_info['size'],
                    modified_time=file_info['modified_time'],
                    is_folder=file_info['is_folder'],
                    file_type=file_info['file_type']
                ))
            return files
        except Exception as e:
            raise FileNotFound(f"列出文件失败: {str(e)}")

    def create_file(self, file_path: str) -> bool:
        """
        创建文件

        Args:
            file_path: 文件路径

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(file_path)
            self.validator.validate_filename(os.path.basename(file_path))

            if os.path.exists(file_path):
                raise FileExists(file_path)

            Path(file_path).touch()
            return True
        except Exception as e:
            raise FilePermissionDenied(f"创建文件失败: {str(e)}")

    def read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """
        读取文件内容

        Args:
            file_path: 文件路径
            encoding: 文件编码

        Returns:
            文件内容
        """
        try:
            self.validator.validate_path(file_path)
            self.validator.validate_file_exists(file_path)

            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            raise FilePermissionDenied(f"读取文件失败: {str(e)}")

    def write_file(self, file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """
        写入文件内容

        Args:
            file_path: 文件路径
            content: 文件内容
            encoding: 文件编码

        Returns:
            操作是否成功
        """
        try:
            self.validator.validate_path(file_path)
            self.validator.validate_file_permission(file_path)

            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            raise FilePermissionDenied(f"写入文件失败: {str(e)}")