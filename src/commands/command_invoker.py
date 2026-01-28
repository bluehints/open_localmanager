from typing import List, Optional
from .base_command import BaseCommand


class CommandInvoker:
    """命令调用器"""

    def __init__(self, max_history: int = 50):
        """
        初始化命令调用器

        Args:
            max_history: 最大历史记录数
        """
        self._undo_stack: List[BaseCommand] = []
        self._redo_stack: List[BaseCommand] = []
        self._max_history = max_history

    def execute_command(self, command: BaseCommand) -> bool:
        """
        执行命令

        Args:
            command: 命令

        Returns:
            执行是否成功
        """
        if command.execute():
            self._undo_stack.append(command)
            self._redo_stack.clear()

            if len(self._undo_stack) > self._max_history:
                self._undo_stack.pop(0)

            return True
        return False

    def undo(self) -> bool:
        """
        撤销上一个命令

        Returns:
            撤销是否成功
        """
        if not self._undo_stack:
            return False

        command = self._undo_stack.pop()
        if command.undo():
            self._redo_stack.append(command)
            return True
        else:
            self._undo_stack.append(command)
            return False

    def redo(self) -> bool:
        """
        重做上一个撤销的命令

        Returns:
            重做是否成功
        """
        if not self._redo_stack:
            return False

        command = self._redo_stack.pop()
        if command.redo():
            self._undo_stack.append(command)
            return True
        else:
            self._redo_stack.append(command)
            return False

    def can_undo(self) -> bool:
        """
        是否可以撤销

        Returns:
            是否可以撤销
        """
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        """
        是否可以重做

        Returns:
            是否可以重做
        """
        return len(self._redo_stack) > 0

    def get_undo_description(self) -> Optional[str]:
        """
        获取撤销命令的描述

        Returns:
            撤销命令的描述
        """
        if self._undo_stack:
            return self._undo_stack[-1].get_description()
        return None

    def get_redo_description(self) -> Optional[str]:
        """
        获取重做命令的描述

        Returns:
            重做命令的描述
        """
        if self._redo_stack:
            return self._redo_stack[-1].get_description()
        return None

    def clear_history(self) -> None:
        """清空历史记录"""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def get_history_count(self) -> int:
        """
        获取历史记录数量

        Returns:
            历史记录数量
        """
        return len(self._undo_stack)