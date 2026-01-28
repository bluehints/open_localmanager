from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileItem:
    """文件项"""

    path: str
    name: str
    size: int
    modified_time: datetime
    is_folder: bool
    file_type: str

    def get_size_str(self) -> str:
        """
        获取格式化的文件大小

        Returns:
            格式化的文件大小
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if self.size < 1024.0:
                return f"{self.size:.2f} {unit}"
            self.size /= 1024.0
        return f"{self.size:.2f} PB"

    def get_modified_time_str(self) -> str:
        """
        获取格式化的修改时间

        Returns:
            格式化的修改时间
        """
        return self.modified_time.strftime("%Y-%m-%d %H:%M:%S")