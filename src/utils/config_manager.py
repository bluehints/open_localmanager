import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.config_model import ConfigModel
from validators.config_validator import ConfigValidator
from exceptions.config_exception import ConfigException


class ConfigManager:
    """配置管理器，负责应用程序配置的加载、保存和管理"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            self.config_path = self._get_default_config_path()
        else:
            self.config_path = config_path

        self.config = ConfigModel()
        self.validator = ConfigValidator()
        self._load_config()

    def _get_default_config_path(self) -> str:
        """
        获取默认配置文件路径

        Returns:
            配置文件路径
        """
        app_dir = Path.home() / '.open_localmanager'
        app_dir.mkdir(exist_ok=True)
        return str(app_dir / 'config.json')

    def _load_config(self) -> None:
        """加载配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_dict = json.load(f)
                    self.config = ConfigModel.from_dict(config_dict)
                    if not self.validator.validate(self.config):
                        self.config = ConfigModel()
            except Exception as e:
                raise ConfigException(f"加载配置失败: {str(e)}")

    def _save_config(self) -> None:
        """保存配置"""
        try:
            config_dict = self.config.to_dict()
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ConfigException(f"保存配置失败: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return getattr(self.config, key, default)

    def set(self, key: str, value: Any) -> None:
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        if hasattr(self.config, key):
            setattr(self.config, key, value)
            self._save_config()

    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置

        Returns:
            所有配置
        """
        return self.config.to_dict()

    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        更新配置

        Args:
            config_dict: 配置字典
        """
        for key, value in config_dict.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self._save_config()

    def reset(self) -> None:
        """重置配置"""
        self.config = ConfigModel()
        self._save_config()

    def reload(self) -> None:
        """重新加载配置"""
        self._load_config()

    def get_config(self) -> ConfigModel:
        """
        获取配置模型

        Returns:
            配置模型
        """
        return self.config

    def set_config(self, config: ConfigModel) -> None:
        """
        设置配置模型

        Args:
            config: 配置模型
        """
        if self.validator.validate(config):
            self.config = config
            self._save_config()

    def get_window_size(self) -> tuple:
        """
        获取窗口大小

        Returns:
            窗口大小 (width, height)
        """
        return (self.config.window_width, self.config.window_height)

    def set_window_size(self, width: int, height: int) -> None:
        """
        设置窗口大小

        Args:
            width: 窗口宽度
            height: 窗口高度
        """
        self.config.window_width = width
        self.config.window_height = height
        self._save_config()

    def get_window_position(self) -> tuple:
        """
        获取窗口位置

        Returns:
            窗口位置 (x, y)
        """
        return (self.config.window_x, self.config.window_y)

    def set_window_position(self, x: int, y: int) -> None:
        """
        设置窗口位置

        Args:
            x: x坐标
            y: y坐标
        """
        self.config.window_x = x
        self.config.window_y = y
        self._save_config()

    def get_sidebar_width(self) -> int:
        """
        获取侧边栏宽度

        Returns:
            侧边栏宽度
        """
        return self.config.sidebar_width

    def set_sidebar_width(self, width: int) -> None:
        """
        设置侧边栏宽度

        Args:
            width: 侧边栏宽度
        """
        self.config.sidebar_width = width
        self._save_config()

    def get_preview_width(self) -> int:
        """
        获取预览区宽度

        Returns:
            预览区宽度
        """
        return self.config.preview_width

    def set_preview_width(self, width: int) -> None:
        """
        设置预览区宽度

        Args:
            width: 预览区宽度
        """
        self.config.preview_width = width
        self._save_config()

    def get_show_hidden_files(self) -> bool:
        """
        获取是否显示隐藏文件

        Returns:
            是否显示隐藏文件
        """
        return self.config.show_hidden_files

    def set_show_hidden_files(self, show: bool) -> None:
        """
        设置是否显示隐藏文件

        Args:
            show: 是否显示隐藏文件
        """
        self.config.show_hidden_files = show
        self._save_config()

    def get_last_open_path(self) -> str:
        """
        获取最后打开的路径

        Returns:
            最后打开的路径
        """
        return self.config.last_open_path

    def set_last_open_path(self, path: str) -> None:
        """
        设置最后打开的路径

        Args:
            path: 路径
        """
        self.config.last_open_path = path
        self._save_config()

    def get_recent_paths(self) -> list:
        """
        获取最近打开的路径列表

        Returns:
            最近打开的路径列表
        """
        return self.config.recent_paths

    def add_recent_path(self, path: str) -> None:
        """
        添加最近打开的路径

        Args:
            path: 路径
        """
        if path in self.config.recent_paths:
            self.config.recent_paths.remove(path)
        self.config.recent_paths.insert(0, path)
        if len(self.config.recent_paths) > 10:
            self.config.recent_paths = self.config.recent_paths[:10]
        self._save_config()

    def clear_recent_paths(self) -> None:
        """清空最近打开的路径列表"""
        self.config.recent_paths = []
        self._save_config()

    def get_theme(self) -> str:
        """
        获取主题

        Returns:
            主题名称
        """
        return self.config.theme

    def set_theme(self, theme: str) -> None:
        """
        设置主题

        Args:
            theme: 主题名称
        """
        self.config.theme = theme
        self._save_config()

    def get_language(self) -> str:
        """
        获取语言

        Returns:
            语言代码
        """
        return self.config.language

    def set_language(self, language: str) -> None:
        """
        设置语言

        Args:
            language: 语言代码
        """
        self.config.language = language
        self._save_config()

    def get_auto_save(self) -> bool:
        """
        获取是否自动保存

        Returns:
            是否自动保存
        """
        return self.config.auto_save

    def set_auto_save(self, auto_save: bool) -> None:
        """
        设置是否自动保存

        Args:
            auto_save: 是否自动保存
        """
        self.config.auto_save = auto_save
        self._save_config()

    def get_auto_save_interval(self) -> int:
        """
        获取自动保存间隔

        Returns:
            自动保存间隔（秒）
        """
        return self.config.auto_save_interval

    def set_auto_save_interval(self, interval: int) -> None:
        """
        设置自动保存间隔

        Args:
            interval: 自动保存间隔（秒）
        """
        self.config.auto_save_interval = interval
        self._save_config()

    def get_log_level(self) -> str:
        """
        获取日志级别

        Returns:
            日志级别
        """
        return self.config.log_level

    def set_log_level(self, level: str) -> None:
        """
        设置日志级别

        Args:
            level: 日志级别
        """
        self.config.log_level = level
        self._save_config()

    def get_log_file_max_size(self) -> int:
        """
        获取日志文件最大大小

        Returns:
            日志文件最大大小（字节）
        """
        return self.config.log_file_max_size

    def set_log_file_max_size(self, size: int) -> None:
        """
        设置日志文件最大大小

        Args:
            size: 日志文件最大大小（字节）
        """
        self.config.log_file_max_size = size
        self._save_config()

    def get_log_file_backup_count(self) -> int:
        """
        获取日志文件备份数量

        Returns:
            日志文件备份数量
        """
        return self.config.log_file_backup_count

    def set_log_file_backup_count(self, count: int) -> None:
        """
        设置日志文件备份数量

        Args:
            count: 日志文件备份数量
        """
        self.config.log_file_backup_count = count
        self._save_config()

    def export_config(self, export_path: str) -> None:
        """
        导出配置

        Args:
            export_path: 导出路径
        """
        try:
            config_dict = self.config.to_dict()
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ConfigException(f"导出配置失败: {str(e)}")

    def import_config(self, import_path: str) -> None:
        """
        导入配置

        Args:
            import_path: 导入路径
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
                self.config = ConfigModel.from_dict(config_dict)
                if not self.validator.validate(self.config):
                    raise ConfigException("导入的配置无效")
                self._save_config()
        except Exception as e:
            raise ConfigException(f"导入配置失败: {str(e)}")