import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from .base_command import BaseCommand
from services.file_service import FileService
from services.folder_service import FolderService


class CopyCommand(BaseCommand):
    """复制命令"""

    def __init__(self, src_path: str, dst_path: str, overwrite: bool = False):
        """
        初始化复制命令

        Args:
            src_path: 源路径
            dst_path: 目标路径
            overwrite: 是否覆盖
        """
        super().__init__()
        self.src_path = src_path
        self.dst_path = dst_path
        self.overwrite = overwrite
        self.file_service = FileService()
        self.folder_service = FolderService()
        self.is_folder = os.path.isdir(src_path)

    def execute(self) -> bool:
        """
        执行复制命令

        Returns:
            执行是否成功
        """
        try:
            if self.is_folder:
                self.folder_service.copy_folder(self.src_path, self.dst_path, self.overwrite)
            else:
                self.file_service.copy_file(self.src_path, self.dst_path, self.overwrite)
            self._set_executed(True)
            return True
        except Exception:
            return False

    def undo(self) -> bool:
        """
        撤销复制命令

        Returns:
            撤销是否成功
        """
        if not self.is_executed():
            return False

        try:
            if os.path.exists(self.dst_path):
                if self.is_folder:
                    self.folder_service.delete_folder(self.dst_path, use_recycle_bin=False, recursive=True)
                else:
                    self.file_service.delete_file(self.dst_path, use_recycle_bin=False)
            self._set_executed(False)
            return True
        except Exception:
            return False

    def redo(self) -> bool:
        """
        重做复制命令

        Returns:
            重做是否成功
        """
        return self.execute()

    def get_description(self) -> str:
        """
        获取命令描述

        Returns:
            命令描述
        """
        item_type = "文件夹" if self.is_folder else "文件"
        return f"复制{item_type}: {self.src_path} -> {self.dst_path}"