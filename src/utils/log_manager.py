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

    def debug(self, message: str) -> None:
        """
        记录调试信息

        Args:
            message: 日志消息
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """
        记录信息

        Args:
            message: 日志消息
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """
        记录警告信息

        Args:
            message: 日志消息
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """
        记录错误信息

        Args:
            message: 日志消息
        """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """
        记录严重错误信息

        Args:
            message: 日志消息
        """
        self.logger.critical(message)

    def exception(self, message: str, exc_info: bool = True) -> None:
        """
        记录异常信息

        Args:
            message: 日志消息
            exc_info: 是否包含异常信息
        """
        self.logger.exception(message, exc_info=exc_info)

    def set_level(self, level: str) -> None:
        """
        设置日志级别

        Args:
            level: 日志级别
        """
        self.config.log_level = level
        self.logger.setLevel(self.config.get_log_level())
        for handler in self.logger.handlers:
            handler.setLevel(self.config.get_log_level())

    def get_log_files(self) -> list:
        """
        获取日志文件列表

        Returns:
            日志文件列表
        """
        log_dir = Path(self.config.log_file_path).parent
        log_files = []
        for file in os.listdir(log_dir):
            if file.startswith('app.log') or (file.startswith('app.log.') and file.endswith('.log')):
                log_files.append(os.path.join(log_dir, file))
        return sorted(log_files, reverse=True)

    def clear_logs(self) -> bool:
        """
        清空日志文件

        Returns:
            清空是否成功
        """
        try:
            log_dir = Path(self.config.log_file_path).parent
            for file in os.listdir(log_dir):
                if file.startswith('app.log') or (file.startswith('app.log.') and file.endswith('.log')):
                    file_path = os.path.join(log_dir, file)
                    os.remove(file_path)
            return True
        except Exception:
            return False

    def get_log_content(self, log_file: str) -> Optional[str]:
        """
        获取日志文件内容

        Args:
            log_file: 日志文件路径

        Returns:
            日志内容
        """
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None