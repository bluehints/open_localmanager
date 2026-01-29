import json
import os
from typing import Optional, Dict, Any
from pathlib import Path


class ConfigManager:
    """配置管理器，负责应用程序配置的加载、保存和管理"""

    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件名
        """
        self.config_file = config_file
        self.config_dir = self._get_config_dir()
        self.config_path = os.path.join(self.config_dir, self.config_file)
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _get_config_dir(self) -> str:
        """
        获取配置目录

        Returns:
            配置目录路径
        """
        app_data_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
        config_dir = os.path.join(app_data_dir, 'OpenLocalManager')
        
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        return config_dir

    def _load_config(self):
        """加载配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except Exception:
                self._config = {}

    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值

        Returns:
            是否成功
        """
        self._config[key] = value
        self._save_config()
        return True

    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置

        Returns:
            所有配置
        """
        return self._config.copy()

    def set_all(self, config: Dict[str, Any]):
        """
        设置所有配置

        Args:
            config: 配置字典
        """
        self._config = config.copy()
        self._save_config()

    def remove(self, key: str):
        """
        删除配置项

        Args:
            key: 配置键
        """
        if key in self._config:
            del self._config[key]
            self._save_config()

    def clear(self):
        """清空配置"""
        self._config = {}
        self._save_config()

    def has(self, key: str) -> bool:
        """
        检查配置项是否存在

        Args:
            key: 配置键

        Returns:
            是否存在
        """
        return key in self._config

    def get_config_path(self) -> str:
        """
        获取配置文件路径

        Returns:
            配置文件路径
        """
        return self.config_path

    def reload(self):
        """重新加载配置"""
        self._load_config()

    def get_config(self) -> Dict[str, Any]:
        """
        获取配置字典

        Returns:
            配置字典
        """
        return self._config.copy()

    def set_config(self, config: Dict[str, Any]) -> bool:
        """
        设置配置字典

        Args:
            config: 配置字典

        Returns:
            是否成功
        """
        self._config = config.copy()
        self._save_config()
        return True

    def reset_to_default(self) -> bool:
        """
        重置为默认配置

        Returns:
            是否成功
        """
        default_config = {
            'current_path': '',
            'show_hidden': False,
            'window_size': {'width': 1200, 'height': 800}
        }
        self._config = default_config.copy()
        self._save_config()
        return True
