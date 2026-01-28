import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from .base_command import BaseCommand
from services.file_service import FileService
from services.folder_service import FolderService


class MoveCommand(BaseCommand):
    """移动命令"""

    def __init__(self, src_path: str, dst_path: str, overwrite: bool = False):
        """
        初始化移动命令

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
        self.original_dst_existed = os.path.exists(dst_path)

    def execute(self) -> bool:
        """
        执行移动命令

        Returns:
            执行是否成功
        """
        try:
            if self.is_folder:
                self.folder_service.move_folder(self.src_path, self.dst_path, self.overwrite)
            else:
                self.file_service.move_file(self.src_path, self.dst_path, self.overwrite)
            self._set_executed(True)
            return True
        except Exception:
            return False

    def undo(self) -> bool:
        """
        撤销移动命令

        Returns:
            撤销是否成功
        """
        if not self.is_executed():
            return False

        try:
            if os.path.exists(self.dst_path):
                if self.is_folder:
                    self.folder_service.move_folder(self.dst_path, self.src_path, True)
                else:
                    self.file_service.move_file(self.dst_path, self.src_path, True)
            self._set_executed(False)
            return True
        except Exception:
            return False

    def redo(self) -> bool:
        """
        重做移动命令

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
        return f"移动{item_type}: {self.src_path} -> {self.dst_path}"