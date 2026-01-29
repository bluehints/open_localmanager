from typing import List, Optional
import os
from pathlib import Path
from models.file_item import FileItem


class SearchService:
    """文件搜索服务"""

    def __init__(self):
        """初始化搜索服务"""
        pass

    def search_files(self, root_path: str, search_text: str, recursive: bool = True) -> List[FileItem]:
        """
        搜索文件

        Args:
            root_path: 根路径
            search_text: 搜索文本
            recursive: 是否递归搜索

        Returns:
            文件列表
        """
        if not os.path.exists(root_path):
            return []

        results = []
        search_lower = search_text.lower()

        if recursive:
            results = self._search_recursive(root_path, search_lower)
        else:
            results = self._search_non_recursive(root_path, search_lower)

        return results

    def _search_recursive(self, path: str, search_text: str) -> List[FileItem]:
        """
        递归搜索

        Args:
            path: 路径
            search_text: 搜索文本

        Returns:
            文件列表
        """
        results = []

        try:
            for entry in os.listdir(path):
                entry_path = os.path.join(path, entry)

                if os.path.isdir(entry_path):
                    if search_text in entry.lower():
                        results.append(self._create_file_item(entry_path, entry, True))
                    results.extend(self._search_recursive(entry_path, search_text))
                elif os.path.isfile(entry_path):
                    if search_text in entry.lower():
                        results.append(self._create_file_item(entry_path, entry, False))
        except Exception:
            pass

        return results

    def _search_non_recursive(self, path: str, search_text: str) -> List[FileItem]:
        """
        非递归搜索

        Args:
            path: 路径
            search_text: 搜索文本

        Returns:
            文件列表
        """
        results = []

        try:
            for entry in os.listdir(path):
                entry_path = os.path.join(path, entry)

                if search_text in entry.lower():
                    is_folder = os.path.isdir(entry_path)
                    results.append(self._create_file_item(entry_path, entry, is_folder))
        except Exception:
            pass

        return results

    def _create_file_item(self, path: str, name: str, is_folder: bool) -> FileItem:
        """
        创建文件项

        Args:
            path: 路径
            name: 名称
            is_folder: 是否是文件夹

        Returns:
            文件项
        """
        try:
            stat_info = os.stat(path)
            size = stat_info.st_size
            modified_time = stat_info.st_mtime
            
            if is_folder:
                file_type = "文件夹"
            else:
                file_type = self._get_file_type(name)

            return FileItem(
                path=path,
                name=name,
                size=size,
                modified_time=modified_time,
                is_folder=is_folder,
                file_type=file_type
            )
        except Exception:
            return FileItem(
                path=path,
                name=name,
                size=0,
                modified_time=0,
                is_folder=is_folder,
                file_type="未知"
            )

    def _get_file_type(self, filename: str) -> str:
        """
        获取文件类型

        Args:
            filename: 文件名

        Returns:
            文件类型
        """
        if '.' not in filename:
            return "文件"

        ext = filename.rsplit('.', 1)[-1].lower()

        type_map = {
            'txt': '文本文件',
            'pdf': 'PDF文档',
            'doc': 'Word文档',
            'docx': 'Word文档',
            'xls': 'Excel表格',
            'xlsx': 'Excel表格',
            'ppt': 'PowerPoint演示',
            'pptx': 'PowerPoint演示',
            'jpg': '图片',
            'jpeg': '图片',
            'png': '图片',
            'gif': '图片',
            'bmp': '图片',
            'mp3': '音频',
            'wav': '音频',
            'flac': '音频',
            'mp4': '视频',
            'avi': '视频',
            'mkv': '视频',
            'mov': '视频',
            'zip': '压缩文件',
            'rar': '压缩文件',
            '7z': '压缩文件',
            'tar': '压缩文件',
            'gz': '压缩文件',
            'exe': '可执行文件',
            'msi': '安装程序',
            'dll': '动态链接库',
            'so': '动态链接库',
            'py': 'Python脚本',
            'js': 'JavaScript文件',
            'html': 'HTML文件',
            'css': 'CSS样式表',
            'json': 'JSON数据',
            'xml': 'XML文件',
            'sql': 'SQL数据库',
            'db': '数据库文件',
            'sqlite': 'SQLite数据库',
            'log': '日志文件',
            'tmp': '临时文件',
            'bak': '备份文件'
        }

        return type_map.get(ext, f'{ext.upper()}文件')