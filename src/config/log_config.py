from dataclasses import dataclass
from typing import Optional


@dataclass
class LogConfig:
    """
    日志配置
    定义日志配置项
    """

    log_level: str = "INFO"
    log_file_path: str = ""
    log_file_max_size: int = 10485760
    log_file_backup_count: int = 5
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    console_output: bool = True
    file_output: bool = True

    def __post_init__(self):
        """初始化后处理"""
        if not self.log_file_path:
            from pathlib import Path
            log_dir = Path.home() / '.open_localmanager' / 'logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            self.log_file_path = str(log_dir / 'app.log')

    def get_log_level(self) -> int:
        """
        获取日志级别数值

        Returns:
            日志级别数值
        """
        level_map = {
            'DEBUG': 10,
            'INFO': 20,
            'WARNING': 30,
            'ERROR': 40,
            'CRITICAL': 50
        }
        return level_map.get(self.log_level.upper(), 20)

    def is_valid(self) -> bool:
        """
        验证配置是否有效

        Returns:
            是否有效
        """
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level.upper() not in valid_levels:
            return False

        if self.log_file_max_size < 1024:
            return False

        if self.log_file_backup_count < 1 or self.log_file_backup_count > 20:
            return False

        return True