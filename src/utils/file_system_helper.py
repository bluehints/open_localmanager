import os
import shutil
import platform
from pathlib import Path
from typing import List, Optional, Tuple


class FileSystemHelper:
    """文件系统辅助工具"""

    @staticmethod
    def is_hidden(file_path: str) -> bool:
        """
        判断文件是否隐藏

        Args:
            file_path: 文件路径

        Returns:
            是否隐藏
        """
        file_name = os.path.basename(file_path)
        if platform.system() == 'Windows':
            return file_name.startswith('.')
        else:
            return file_name.startswith('.')

    @staticmethod
    def get_file_size_str(size: int) -> str:
        """
        格式化文件大小

        Args:
            size: 文件大小（字节）

        Returns:
            格式化后的文件大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """
        获取文件扩展名

        Args:
            file_path: 文件路径

        Returns:
            文件扩展名
        """
        return os.path.splitext(file_path)[1].lower()

    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """
        判断文件名是否有效

        Args:
            filename: 文件名

        Returns:
            是否有效
        """
        invalid_chars = '<>:"|?*'
        for char in invalid_chars:
            if char in filename:
                return False
        return True

    @staticmethod
    def get_unique_filename(directory: str, filename: str) -> str:
        """
        获取唯一的文件名

        Args:
            directory: 目录
            filename: 文件名

        Returns:
            唯一的文件名
        """
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while os.path.exists(os.path.join(directory, new_filename)):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1

        return new_filename

    @staticmethod
    def get_directory_size(directory: str) -> int:
        """
        获取目录大小

        Args:
            directory: 目录路径

        Returns:
            目录大小（字节）
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
        return total_size

    @staticmethod
    def get_file_count(directory: str) -> Tuple[int, int]:
        """
        获取文件和文件夹数量

        Args:
            directory: 目录路径

        Returns:
            (文件数量, 文件夹数量)
        """
        file_count = 0
        folder_count = 0

        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry)
            if os.path.isfile(entry_path):
                file_count += 1
            elif os.path.isdir(entry_path):
                folder_count += 1

        return file_count, folder_count

    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        获取文件信息

        Args:
            file_path: 文件路径

        Returns:
            文件信息字典
        """
        if not os.path.exists(file_path):
            return {}

        stat_info = os.stat(file_path)
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'size': stat_info.st_size,
            'modified_time': stat_info.st_mtime,
            'created_time': stat_info.st_ctime,
            'is_file': os.path.isfile(file_path),
            'is_directory': os.path.isdir(file_path)
        }

    @staticmethod
    def get_folder_info(folder_path: str) -> dict:
        """
        获取文件夹信息

        Args:
            folder_path: 文件夹路径

        Returns:
            文件夹信息字典
        """
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return {}

        stat_info = os.stat(folder_path)
        file_count, folder_count = FileSystemHelper.get_file_count(folder_path)
        total_size = FileSystemHelper.get_directory_size(folder_path)

        return {
            'path': folder_path,
            'name': os.path.basename(folder_path),
            'size': total_size,
            'modified_time': stat_info.st_mtime,
            'created_time': stat_info.st_ctime,
            'file_count': file_count,
            'folder_count': folder_count
        }

    @staticmethod
    def get_disk_usage(path: str) -> dict:
        """
        获取磁盘使用情况

        Args:
            path: 路径

        Returns:
            磁盘使用信息字典
        """
        if platform.system() == 'Windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            drive = os.path.splitdrive(path)[0] + '\\'
            try:
                free = ctypes.c_ulonglong(0)
                total = ctypes.c_ulonglong(0)
                available = ctypes.c_ulonglong(0)
                kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(drive),
                    ctypes.byref(free),
                    ctypes.byref(total),
                    ctypes.byref(available)
                )
                return {
                    'path': drive,
                    'free': free.value,
                    'total': total.value,
                    'used': total.value - free.value
                }
            except Exception:
                return {
                    'path': drive,
                    'free': 0,
                    'total': 0,
                    'used': 0
                }
        else:
            stat = os.statvfs(path)
            total = stat.f_frsize * stat.f_blocks
            free = stat.f_bfree * stat.f_frsize
            return {
                'path': path,
                'free': free,
                'total': total,
                'used': total - free
            }

    @staticmethod
    def get_drive_info() -> List[dict]:
        """
        获取驱动器信息

        Returns:
            驱动器信息列表
        """
        drives = []
        if platform.system() == 'Windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            bitmask = kernel32.GetLogicalDrives()
            for i in range(26):
                if bitmask & (1 << i):
                    drive = chr(65 + i) + ':\\'
                    try:
                        free = ctypes.c_ulonglong(0)
                        total = ctypes.c_ulonglong(0)
                        available = ctypes.c_ulonglong(0)
                        kernel32.GetDiskFreeSpaceExW(
                            ctypes.c_wchar_p(drive),
                            ctypes.byref(free),
                            ctypes.byref(total),
                            ctypes.byref(available)
                        )
                        drives.append({
                            'path': drive,
                            'label': drive,
                            'free': free.value,
                            'total': total.value,
                            'used': total.value - free.value
                        })
                    except Exception:
                        drives.append({
                            'path': drive,
                            'label': drive,
                            'free': 0,
                            'total': 0,
                            'used': 0
                        })
        else:
            for mount in ['/']:
                if os.path.ismount(mount):
                    stat = os.statvfs(mount)
                    total = stat.f_frsize * stat.f_blocks
                    free = stat.f_bfree * stat.f_frsize
                    drives.append({
                        'path': mount,
                        'label': mount,
                        'free': free,
                        'total': total,
                        'used': total - free
                    })
        return drives

    @staticmethod
    def get_file_type(file_path: str) -> str:
        """
        获取文件类型

        Args:
            file_path: 文件路径

        Returns:
            文件类型
        """
        if os.path.isdir(file_path):
            return '文件夹'
        elif os.path.isfile(file_path):
            ext = FileSystemHelper.get_file_extension(file_path)
            type_map = {
                '.txt': '文本文件',
                '.pdf': 'PDF文档',
                '.doc': 'Word文档',
                '.docx': 'Word文档',
                '.xls': 'Excel表格',
                '.xlsx': 'Excel表格',
                '.ppt': 'PowerPoint演示',
                '.pptx': 'PowerPoint演示',
                '.jpg': '图片',
                '.jpeg': '图片',
                '.png': '图片',
                '.gif': '图片',
                '.bmp': '图片',
                '.mp3': '音频',
                '.wav': '音频',
                '.flac': '音频',
                '.mp4': '视频',
                '.avi': '视频',
                '.mkv': '视频',
                '.mov': '视频',
                '.zip': '压缩文件',
                '.rar': '压缩文件',
                '.7z': '压缩文件',
                '.exe': '可执行文件',
                '.msi': '安装包',
                '.py': 'Python脚本',
                '.js': 'JavaScript文件',
                '.html': 'HTML文件',
                '.css': 'CSS样式表',
                '.json': 'JSON数据',
                '.xml': 'XML文件',
            }
            return type_map.get(ext, '文件')
        return '未知'

    @staticmethod
    def is_same_drive(path1: str, path2: str) -> bool:
        """
        判断两个路径是否在同一驱动器

        Args:
            path1: 路径1
            path2: 路径2

        Returns:
            是否在同一驱动器
        """
        drive1 = os.path.splitdrive(path1)[0]
        drive2 = os.path.splitdrive(path2)[0]
        return drive1 == drive2

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        规范化路径

        Args:
            path: 路径

        Returns:
            规范化后的路径
        """
        return os.path.normpath(os.path.abspath(path))

    @staticmethod
    def join_paths(*paths: str) -> str:
        """
        连接路径

        Args:
            *paths: 路径列表

        Returns:
            连接后的路径
        """
        return os.path.join(*paths)

    @staticmethod
    def get_parent_directory(path: str) -> str:
        """
        获取父目录

        Args:
            path: 路径

        Returns:
            父目录路径
        """
        return os.path.dirname(path)

    @staticmethod
    def get_filename(path: str) -> str:
        """
        获取文件名

        Args:
            path: 路径

        Returns:
            文件名
        """
        return os.path.basename(path)

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
        判断是否是文件

        Args:
            path: 路径

        Returns:
            是否是文件
        """
        return os.path.isfile(path)

    @staticmethod
    def is_directory(path: str) -> bool:
        """
        判断是否是目录

        Args:
            path: 路径

        Returns:
            是否是目录
        """
        return os.path.isdir(path)

    @staticmethod
    def create_directory(path: str) -> bool:
        """
        创建目录

        Args:
            path: 路径

        Returns:
            创建是否成功
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def delete_directory(path: str) -> bool:
        """
        删除目录

        Args:
            path: 路径

        Returns:
            删除是否成功
        """
        try:
            shutil.rmtree(path)
            return True
        except Exception:
            return False

    @staticmethod
    def copy_directory(src: str, dst: str) -> bool:
        """
        复制目录

        Args:
            src: 源路径
            dst: 目标路径

        Returns:
            复制是否成功
        """
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def move_directory(src: str, dst: str) -> bool:
        """
        移动目录

        Args:
            src: 源路径
            dst: 目标路径

        Returns:
            移动是否成功
        """
        try:
            shutil.move(src, dst)
            return True
        except Exception:
            return False