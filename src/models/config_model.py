from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ConfigModel:
    """
    配置模型
    定义应用程序的配置项
    """

    window_width: int = 1200
    window_height: int = 800
    window_x: int = 100
    window_y: int = 100
    sidebar_width: int = 250
    preview_width: int = 300
    show_hidden_files: bool = False
    last_open_path: str = ""
    recent_paths: list = field(default_factory=list)
    theme: str = "default"
    language: str = "zh_CN"
    auto_save: bool = True
    auto_save_interval: int = 300
    log_level: str = "INFO"
    log_file_max_size: int = 10485760
    log_file_backup_count: int = 5

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        Returns:
            配置字典
        """
        return {
            'window_width': self.window_width,
            'window_height': self.window_height,
            'window_x': self.window_x,
            'window_y': self.window_y,
            'sidebar_width': self.sidebar_width,
            'preview_width': self.preview_width,
            'show_hidden_files': self.show_hidden_files,
            'last_open_path': self.last_open_path,
            'recent_paths': self.recent_paths,
            'theme': self.theme,
            'language': self.language,
            'auto_save': self.auto_save,
            'auto_save_interval': self.auto_save_interval,
            'log_level': self.log_level,
            'log_file_max_size': self.log_file_max_size,
            'log_file_backup_count': self.log_file_backup_count
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ConfigModel':
        """
        从字典创建配置模型

        Args:
            config_dict: 配置字典

        Returns:
            配置模型
        """
        return cls(
            window_width=config_dict.get('window_width', 1200),
            window_height=config_dict.get('window_height', 800),
            window_x=config_dict.get('window_x', 100),
            window_y=config_dict.get('window_y', 100),
            sidebar_width=config_dict.get('sidebar_width', 250),
            preview_width=config_dict.get('preview_width', 300),
            show_hidden_files=config_dict.get('show_hidden_files', False),
            last_open_path=config_dict.get('last_open_path', ''),
            recent_paths=config_dict.get('recent_paths', []),
            theme=config_dict.get('theme', 'default'),
            language=config_dict.get('language', 'zh_CN'),
            auto_save=config_dict.get('auto_save', True),
            auto_save_interval=config_dict.get('auto_save_interval', 300),
            log_level=config_dict.get('log_level', 'INFO'),
            log_file_max_size=config_dict.get('log_file_max_size', 10485760),
            log_file_backup_count=config_dict.get('log_file_backup_count', 5)
        )

    def add_recent_path(self, path: str):
        """
        添加最近路径

        Args:
            path: 路径
        """
        if path in self.recent_paths:
            self.recent_paths.remove(path)
        self.recent_paths.insert(0, path)
        if len(self.recent_paths) > 10:
            self.recent_paths = self.recent_paths[:10]

    def clear_recent_paths(self):
        """清除最近路径"""
        self.recent_paths = []