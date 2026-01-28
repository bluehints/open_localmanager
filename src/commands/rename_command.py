import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from .base_command import BaseCommand
from services.file_service import FileService
from services.folder_service import FolderService


class RenameCommand(BaseCommand):
    """重命名命令"""

    def __init__(self, old_path: str, new_path: str, overwrite: bool = False):
        """
        初始化重命名命令

        Args:
            old_path: 原路径
            new_path: 新路径
            overwrite: 是否覆盖
        """
        super().__init__()
        self.old_path = old_path
        self.new_path = new_path
        self.overwrite = overwrite
        self.file_service = FileService()
        self.folder_service = FolderService()
        self.is_folder = os.path.isdir(old_path)

    def execute(self) -> bool:
        """
        执行重命名命令

        Returns:
            执行是否成功
        """
        try:
            if self.is_folder:
                self.folder_service.rename_folder(self.old_path, self.new_path, self.overwrite)
            else:
                self.file_service.rename_file(self.old_path, self.new_path, self.overwrite)
            self._set_executed(True)
            return True
        except Exception:
            return False

    def undo(self) -> bool:
        """
        撤销重命名命令

        Returns:
            撤销是否成功
        """
        if not self.is_executed():
            return False

        try:
            if os.path.exists(self.new_path):
                if self.is_folder:
                    self.folder_service.rename_folder(self.new_path, self.old_path, True)
                else:
                    self.file_service.rename_file(self.new_path, self.old_path, True)
            self._set_executed(False)
            return True
        except Exception:
            return False

    def redo(self) -> bool:
        """
        重做重命名命令

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
        old_name = os.path.basename(self.old_path)
        new_name = os.path.basename(self.new_path)
        return f"重命名{item_type}: {old_name} -> {new_name}"