import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.log_config import LogConfig


class LogManager:
    """日志管理器"""

    def __init__(self, config: Optional[LogConfig] = None):
        """
        初始化日志管理器

        Args:
            config: 日志配置
        """
        self.config = config if config else LogConfig()
        self.logger = None
        self._setup_logger()

    def _setup_logger(self) -> None:
        """设置日志记录器"""
        self.logger = logging.getLogger('OpenLocalManager')
        self.logger.setLevel(self.config.get_log_level())

        formatter = logging.Formatter(
            self.config.log_format,
            datefmt=self.config.date_format
        )

        if self.config.file_output:
            log_file = self.config.log_file_path
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=self.config.log_file_max_size,
                backupCount=self.config.log_file_backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.config.get_log_level())
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if self.config.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.config.get_log_level())
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        """
        获取日志记录器

        Returns:
            日志记录器
        """
        return self.logger

    def debug(self, message: str) -> None:
        """
        记录调试信息

        Args:
            message: 消息内容
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """
        记录信息

        Args:
            message: 消息内容
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """
        记录警告

        Args:
            message: 消息内容
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """
        记录错误

        Args:
            message: 消息内容
        """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """
        记录严重错误

        Args:
            message: 消息内容
        """
        self.logger.critical(message)

    def exception(self, message: str) -> None:
        """
        记录异常

        Args:
            message: 消息内容
        """
        self.logger.exception(message)

    def set_level(self, level: str) -> None:
        """
        设置日志级别

        Args:
            level: 日志级别
        """
        self.logger.setLevel(level)

    def get_level(self) -> str:
        """
        获取日志级别

        Returns:
            日志级别
        """
        return self.logger.level

    def close(self) -> None:
        """关闭日志管理器"""
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)