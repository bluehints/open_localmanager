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
            except Exception:
                self.config = ConfigModel()
        else:
            self.config = ConfigModel()

    def _save_config(self) -> bool:
        """
        保存配置

        Returns:
            保存是否成功
        """
        try:
            config_dict = self.config.to_dict()
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get_config(self) -> ConfigModel:
        """
        获取配置模型

        Returns:
            配置模型
        """
        return self.config

    def set_config(self, config: ConfigModel) -> bool:
        """
        设置配置模型

        Args:
            config: 配置模型

        Returns:
            设置是否成功
        """
        if self.validator.validate(config):
            self.config = config
            return self._save_config()
        return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        config_dict = self.config.to_dict()
        keys = key.split('.')
        value = config_dict

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值

        Returns:
            设置是否成功
        """
        config_dict = self.config.to_dict()
        keys = key.split('.')
        config = config_dict

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.config = ConfigModel.from_dict(config_dict)

        return self._save_config()

    def reset_to_default(self) -> bool:
        """
        重置为默认配置

        Returns:
            重置是否成功
        """
        self.config = ConfigModel()
        return self._save_config()

    def export_config(self, export_path: str) -> bool:
        """
        导出配置

        Args:
            export_path: 导出路径

        Returns:
            导出是否成功
        """
        try:
            config_dict = self.config.to_dict()
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def import_config(self, import_path: str) -> bool:
        """
        导入配置

        Args:
            import_path: 导入路径

        Returns:
            导入是否成功
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
                config = ConfigModel.from_dict(config_dict)
                if self.validator.validate(config):
                    self.config = config
                    return self._save_config()
            return False
        except Exception:
            return False