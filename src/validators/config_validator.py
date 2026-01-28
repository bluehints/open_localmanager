from typing import Dict, Any
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.config_model import ConfigModel
from exceptions.config_exception import ConfigException


class ConfigValidator:
    """
    配置验证器
    验证配置的有效性
    """

    def __init__(self):
        """初始化验证器"""
        self._valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        self._valid_themes = ['default', 'dark', 'light']
        self._valid_languages = ['zh_CN', 'en_US']

    def validate(self, config: ConfigModel) -> bool:
        """
        验证配置

        Args:
            config: 配置模型

        Returns:
            是否有效
        """
        try:
            self._validate_window_size(config.window_width, config.window_height)
            self._validate_window_position(config.window_x, config.window_y)
            self._validate_sidebar_width(config.sidebar_width)
            self._validate_preview_width(config.preview_width)
            self._validate_last_open_path(config.last_open_path)
            self._validate_recent_paths(config.recent_paths)
            self._validate_theme(config.theme)
            self._validate_language(config.language)
            self._validate_auto_save_interval(config.auto_save_interval)
            self._validate_log_level(config.log_level)
            self._validate_log_file_max_size(config.log_file_max_size)
            self._validate_log_file_backup_count(config.log_file_backup_count)
            return True
        except ConfigException:
            return False

    def _validate_window_size(self, width: int, height: int):
        """
        验证窗口大小

        Args:
            width: 宽度
            height: 高度
        """
        if width < 800:
            raise ConfigException("窗口宽度不能小于800")
        if width > 3840:
            raise ConfigException("窗口宽度不能大于3840")
        if height < 600:
            raise ConfigException("窗口高度不能小于600")
        if height > 2160:
            raise ConfigException("窗口高度不能大于2160")

    def _validate_window_position(self, x: int, y: int):
        """
        验证窗口位置

        Args:
            x: X坐标
            y: Y坐标
        """
        if x < 0:
            raise ConfigException("窗口X坐标不能小于0")
        if y < 0:
            raise ConfigException("窗口Y坐标不能小于0")

    def _validate_sidebar_width(self, width: int):
        """
        验证侧边栏宽度

        Args:
            width: 宽度
        """
        if width < 200:
            raise ConfigException("侧边栏宽度不能小于200")
        if width > 600:
            raise ConfigException("侧边栏宽度不能大于600")

    def _validate_preview_width(self, width: int):
        """
        验证预览区宽度

        Args:
            width: 宽度
        """
        if width < 200:
            raise ConfigException("预览区宽度不能小于200")
        if width > 800:
            raise ConfigException("预览区宽度不能大于800")

    def _validate_last_open_path(self, path: str):
        """
        验证最后打开路径

        Args:
            path: 路径
        """
        if path and not Path(path).exists():
            raise ConfigException(f"路径不存在: {path}")

    def _validate_recent_paths(self, paths: list):
        """
        验证最近路径

        Args:
            paths: 路径列表
        """
        if not isinstance(paths, list):
            raise ConfigException("最近路径必须是列表")

        if len(paths) > 20:
            raise ConfigException("最近路径数量不能超过20")

        for path in paths:
            if not isinstance(path, str):
                raise ConfigException("最近路径必须是字符串")
            if path and not Path(path).exists():
                pass

    def _validate_theme(self, theme: str):
        """
        验证主题

        Args:
            theme: 主题
        """
        if theme not in self._valid_themes:
            raise ConfigException(f"无效的主题: {theme}")

    def _validate_language(self, language: str):
        """
        验证语言

        Args:
            language: 语言
        """
        if language not in self._valid_languages:
            raise ConfigException(f"无效的语言: {language}")

    def _validate_auto_save_interval(self, interval: int):
        """
        验证自动保存间隔

        Args:
            interval: 间隔（秒）
        """
        if interval < 60:
            raise ConfigException("自动保存间隔不能小于60秒")
        if interval > 3600:
            raise ConfigException("自动保存间隔不能大于3600秒")

    def _validate_log_level(self, level: str):
        """
        验证日志级别

        Args:
            level: 日志级别
        """
        if level not in self._valid_log_levels:
            raise ConfigException(f"无效的日志级别: {level}")

    def _validate_log_file_max_size(self, size: int):
        """
        验证日志文件最大大小

        Args:
            size: 大小（字节）
        """
        if size < 1024:
            raise ConfigException("日志文件最大大小不能小于1KB")
        if size > 104857600:
            raise ConfigException("日志文件最大大小不能大于100MB")

    def _validate_log_file_backup_count(self, count: int):
        """
        验证日志文件备份数量

        Args:
            count: 备份数量
        """
        if count < 1:
            raise ConfigException("日志文件备份数量不能小于1")
        if count > 20:
            raise ConfigException("日志文件备份数量不能大于20")

    def validate_dict(self, config_dict: Dict[str, Any]) -> bool:
        """
        验证配置字典

        Args:
            config_dict: 配置字典

        Returns:
            是否有效
        """
        try:
            config = ConfigModel.from_dict(config_dict)
            return self.validate(config)
        except Exception:
            return False