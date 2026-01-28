import os
import shutil
import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from .base_command import BaseCommand
from services.file_service import FileService
from services.folder_service import FolderService


class DeleteCommand(BaseCommand):
    """删除命令"""

    def __init__(self, path: str, use_recycle_bin: bool = True, recursive: bool = False):
        """
        初始化删除命令

        Args:
            path: 路径
            use_recycle_bin: 是否使用回收站
            recursive: 是否递归删除
        """
        super().__init__()
        self.path = path
        self.use_recycle_bin = use_recycle_bin
        self.recursive = recursive
        self.file_service = FileService()
        self.folder_service = FolderService()
        self.is_folder = os.path.isdir(path)
        self.backup_path = None

    def execute(self) -> bool:
        """
        执行删除命令

        Returns:
            执行是否成功
        """
        try:
            if not os.path.exists(self.path):
                return False

            if not self.use_recycle_bin:
                self._backup_to_temp()

            if self.is_folder:
                self.folder_service.delete_folder(self.path, self.use_recycle_bin, self.recursive)
            else:
                self.file_service.delete_file(self.path, self.use_recycle_bin)

            self._set_executed(True)
            return True
        except Exception:
            return False

    def undo(self) -> bool:
        """
        撤销删除命令

        Returns:
            撤销是否成功
        """
        if not self.is_executed():
            return False

        try:
            if self.use_recycle_bin:
                return False

            if self.backup_path and os.path.exists(self.backup_path):
                shutil.move(self.backup_path, self.path)
                self.backup_path = None
                self._set_executed(False)
                return True
            return False
        except Exception:
            return False

    def redo(self) -> bool:
        """
        重做删除命令

        Returns:
            重做是否成功
        """
        return self.execute()

    def _backup_to_temp(self) -> None:
        """
        备份到临时目录
        """
        temp_dir = tempfile.gettempdir()
        backup_name = f"backup_{os.path.basename(self.path)}_{id(self)}"
        self.backup_path = os.path.join(temp_dir, backup_name)

        if self.is_folder:
            shutil.copytree(self.path, self.backup_path)
        else:
            shutil.copy2(self.path, self.backup_path)

    def get_description(self) -> str:
        """
        获取命令描述

        Returns:
            命令描述
        """
        item_type = "文件夹" if self.is_folder else "文件"
        method = "回收站" if self.use_recycle_bin else "永久"
        return f"删除{item_type}: {self.path} ({method})"