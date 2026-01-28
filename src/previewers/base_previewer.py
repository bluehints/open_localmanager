from abc import ABC, abstractmethod
from typing import Optional
from PySide6.QtWidgets import QWidget


class BasePreviewer(ABC):
    """预览器基类"""

    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化预览器

        Args:
            parent: 父窗口
        """
        self.parent = parent
        self.current_path: Optional[str] = None

    @abstractmethod
    def can_preview(self, file_path: str) -> bool:
        """
        判断是否可以预览该文件

        Args:
            file_path: 文件路径

        Returns:
            是否可以预览
        """
        pass

    @abstractmethod
    def preview(self, file_path: str) -> bool:
        """
        预览文件

        Args:
            file_path: 文件路径

        Returns:
            预览是否成功
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """清空预览"""
        pass

    @abstractmethod
    def get_widget(self) -> QWidget:
        """
        获取预览窗口部件

        Returns:
            预览窗口部件
        """
        pass

    def get_current_path(self) -> Optional[str]:
        """
        获取当前预览的文件路径

        Returns:
            当前文件路径
        """
        return self.current_path