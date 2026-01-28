from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    """命令基类"""

    def __init__(self):
        """初始化命令"""
        self._executed = False

    @abstractmethod
    def execute(self) -> bool:
        """
        执行命令

        Returns:
            执行是否成功
        """
        pass

    @abstractmethod
    def undo(self) -> bool:
        """
        撤销命令

        Returns:
            撤销是否成功
        """
        pass

    @abstractmethod
    def redo(self) -> bool:
        """
        重做命令

        Returns:
            重做是否成功
        """
        pass

    def is_executed(self) -> bool:
        """
        是否已执行

        Returns:
            是否已执行
        """
        return self._executed

    def _set_executed(self, executed: bool) -> None:
        """
        设置执行状态

        Args:
            executed: 执行状态
        """
        self._executed = executed

    @abstractmethod
    def get_description(self) -> str:
        """
        获取命令描述

        Returns:
            命令描述
        """
        pass