import unittest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from tests.test_base import ComponentTest
from models.config_model import ConfigModel
from validators.config_validator import ConfigValidator
from utils.config_manager import ConfigManager


class TestConfigModule(ComponentTest):
    """配置模块测试"""

    def setUp(self):
        """测试前准备"""
        self.validator = ConfigValidator()

    def test_config_model_creation(self):
        """测试配置模型创建"""
        config = ConfigModel()
        self.assertEqual(config.window_width, 1200)
        self.assertEqual(config.window_height, 800)
        self.assertEqual(config.show_hidden_files, False)

    def test_config_model_to_dict(self):
        """测试配置模型转换为字典"""
        config = ConfigModel()
        config_dict = config.to_dict()
        self.assertIn('window_width', config_dict)
        self.assertIn('window_height', config_dict)
        self.assertEqual(config_dict['window_width'], 1200)

    def test_config_model_from_dict(self):
        """测试从字典创建配置模型"""
        config_dict = {
            'window_width': 1920,
            'window_height': 1080,
            'show_hidden_files': True
        }
        config = ConfigModel.from_dict(config_dict)
        self.assertEqual(config.window_width, 1920)
        self.assertEqual(config.window_height, 1080)
        self.assertEqual(config.show_hidden_files, True)

    def test_config_model_add_recent_path(self):
        """测试添加最近路径"""
        config = ConfigModel()
        config.add_recent_path("/test/path1")
        self.assertEqual(len(config.recent_paths), 1)
        self.assertEqual(config.recent_paths[0], "/test/path1")

        config.add_recent_path("/test/path2")
        self.assertEqual(len(config.recent_paths), 2)
        self.assertEqual(config.recent_paths[0], "/test/path2")

        config.add_recent_path("/test/path1")
        self.assertEqual(len(config.recent_paths), 2)
        self.assertEqual(config.recent_paths[0], "/test/path1")

    def test_config_model_clear_recent_paths(self):
        """测试清除最近路径"""
        config = ConfigModel()
        config.add_recent_path("/test/path1")
        config.add_recent_path("/test/path2")
        self.assertEqual(len(config.recent_paths), 2)

        config.clear_recent_paths()
        self.assertEqual(len(config.recent_paths), 0)

    def test_config_validator_valid_config(self):
        """测试有效配置验证"""
        config = ConfigModel()
        result = self.validator.validate(config)
        self.assertTrue(result)

    def test_config_validator_invalid_window_size(self):
        """测试无效窗口大小验证"""
        config = ConfigModel()
        config.window_width = 700
        result = self.validator.validate(config)
        self.assertFalse(result)

    def test_config_validator_invalid_log_level(self):
        """测试无效日志级别验证"""
        config = ConfigModel()
        config.log_level = "INVALID"
        result = self.validator.validate(config)
        self.assertFalse(result)

    def test_config_manager_creation(self):
        """测试配置管理器创建"""
        manager = ConfigManager()
        self.assertIsNotNone(manager.get_config())

    def test_config_manager_get_set(self):
        """测试配置管理器获取和设置"""
        manager = ConfigManager()
        value = manager.get('window_width')
        self.assertIsNone(value)

        result = manager.set('window_width', 1920)
        self.assertTrue(result)

        value = manager.get('window_width')
        self.assertEqual(value, 1920)

    def test_config_manager_reset(self):
        """测试配置管理器重置"""
        manager = ConfigManager()
        manager.set('window_width', 1920)
        result = manager.reset_to_default()
        self.assertTrue(result)

        window_size = manager.get('window_size')
        self.assertIsNotNone(window_size)
        self.assertEqual(window_size['width'], 1200)

    def test_config_model_docstring(self):
        """测试配置模型文档字符串"""
        self.assert_component_docstring(ConfigModel)

    def test_config_validator_docstring(self):
        """测试配置验证器文档字符串"""
        self.assert_component_docstring(ConfigValidator)

    def test_config_manager_docstring(self):
        """测试配置管理器文档字符串"""
        self.assert_component_docstring(ConfigManager)


if __name__ == '__main__':
    unittest.main()
