import unittest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from tests.test_base import ComponentTest
from services.file_service import FileService
from services.folder_service import FolderService
from services.tree_service import TreeService
from services.preview_service import PreviewService
from utils.config_manager import ConfigManager
from utils.log_manager import LogManager
from utils.clipboard_manager import ClipboardManager
from utils.icon_provider import IconProvider
from utils.file_system_helper import FileSystemHelper
from utils.tree_loader import TreeLoader
from models.file_item import FileItem
from models.tree_item import TreeItem
from models.config_model import ConfigModel
from config.log_config import LogConfig
from validators.file_validator import FileValidator
from validators.folder_validator import FolderValidator
from validators.config_validator import ConfigValidator
from commands.base_command import BaseCommand
from commands.copy_command import CopyCommand
from commands.move_command import MoveCommand
from commands.delete_command import DeleteCommand
from commands.rename_command import RenameCommand
from commands.command_invoker import CommandInvoker
from signals.sidebar_signals import SidebarSignals
from signals.file_manager_signals import FileManagerSignals
from signals.preview_signals import PreviewSignals
from signals.file_operation_signals import FileOperationSignals
from signals.main_window_signals import MainWindowSignals


class TestFileServiceInterface(ComponentTest):
    """文件服务接口测试"""

    def setUp(self):
        """测试前准备"""
        self.service = FileService()

    def test_file_service_has_copy_file_method(self):
        """测试文件服务有复制文件方法"""
        self.assert_component_has_method(self.service, 'copy_file')

    def test_file_service_has_move_file_method(self):
        """测试文件服务有移动文件方法"""
        self.assert_component_has_method(self.service, 'move_file')

    def test_file_service_has_delete_file_method(self):
        """测试文件服务有删除文件方法"""
        self.assert_component_has_method(self.service, 'delete_file')

    def test_file_service_has_rename_file_method(self):
        """测试文件服务有重命名文件方法"""
        self.assert_component_has_method(self.service, 'rename_file')

    def test_file_service_has_create_file_method(self):
        """测试文件服务有创建文件方法"""
        self.assert_component_has_method(self.service, 'create_file')

    def test_file_service_has_get_file_info_method(self):
        """测试文件服务有获取文件信息方法"""
        self.assert_component_has_method(self.service, 'get_file_info')

    def test_file_service_has_list_files_method(self):
        """测试文件服务有列出文件方法"""
        self.assert_component_has_method(self.service, 'list_files')


class TestFolderServiceInterface(ComponentTest):
    """文件夹服务接口测试"""

    def setUp(self):
        """测试前准备"""
        self.service = FolderService()

    def test_folder_service_has_create_folder_method(self):
        """测试文件夹服务有创建文件夹方法"""
        self.assert_component_has_method(self.service, 'create_folder')

    def test_folder_service_has_delete_folder_method(self):
        """测试文件夹服务有删除文件夹方法"""
        self.assert_component_has_method(self.service, 'delete_folder')

    def test_folder_service_has_list_folders_method(self):
        """测试文件夹服务有列出文件夹方法"""
        self.assert_component_has_method(self.service, 'list_folders')


class TestTreeServiceInterface(ComponentTest):
    """树形结构服务接口测试"""

    def setUp(self):
        """测试前准备"""
        self.service = TreeService()

    def test_tree_service_has_load_tree_method(self):
        """测试树形结构服务有加载树方法"""
        self.assert_component_has_method(self.service, 'load_tree')

    def test_tree_service_has_load_children_method(self):
        """测试树形结构服务有加载子节点方法"""
        self.assert_component_has_method(self.service, 'load_children')

    def test_tree_service_has_select_node_method(self):
        """测试树形结构服务有选中节点方法"""
        self.assert_component_has_method(self.service, 'select_node')

    def test_tree_service_has_find_item_method(self):
        """测试树形结构服务有查找节点方法"""
        self.assert_component_has_method(self.service, 'find_item')


class TestPreviewServiceInterface(ComponentTest):
    """预览服务接口测试"""

    def setUp(self):
        """测试前准备"""
        self.service = PreviewService()

    def test_preview_service_has_preview_file_method(self):
        """测试预览服务有预览文件方法"""
        self.assert_component_has_method(self.service, 'preview_file')

    def test_preview_service_has_clear_preview_method(self):
        """测试预览服务有清除预览方法"""
        self.assert_component_has_method(self.service, 'clear_preview')

    def test_preview_service_has_get_widget_method(self):
        """测试预览服务有获取组件方法"""
        self.assert_component_has_method(self.service, 'get_widget')


class TestConfigManagerInterface(ComponentTest):
    """配置管理器接口测试"""

    def setUp(self):
        """测试前准备"""
        self.manager = ConfigManager()

    def test_config_manager_has_get_config_method(self):
        """测试配置管理器有获取配置方法"""
        self.assert_component_has_method(self.manager, 'get_config')

    def test_config_manager_has_set_config_method(self):
        """测试配置管理器有设置配置方法"""
        self.assert_component_has_method(self.manager, 'set_config')

    def test_config_manager_has_get_method(self):
        """测试配置管理器有获取配置项方法"""
        self.assert_component_has_method(self.manager, 'get')

    def test_config_manager_has_set_method(self):
        """测试配置管理器有设置配置项方法"""
        self.assert_component_has_method(self.manager, 'set')

    def test_config_manager_has_reset_to_default_method(self):
        """测试配置管理器有重置为默认方法"""
        self.assert_component_has_method(self.manager, 'reset_to_default')


class TestLogManagerInterface(ComponentTest):
    """日志管理器接口测试"""

    def setUp(self):
        """测试前准备"""
        self.manager = LogManager()

    def test_log_manager_has_debug_method(self):
        """测试日志管理器有调试方法"""
        self.assert_component_has_method(self.manager, 'debug')

    def test_log_manager_has_info_method(self):
        """测试日志管理器有信息方法"""
        self.assert_component_has_method(self.manager, 'info')

    def test_log_manager_has_warning_method(self):
        """测试日志管理器有警告方法"""
        self.assert_component_has_method(self.manager, 'warning')

    def test_log_manager_has_error_method(self):
        """测试日志管理器有错误方法"""
        self.assert_component_has_method(self.manager, 'error')

    def test_log_manager_has_critical_method(self):
        """测试日志管理器有严重错误方法"""
        self.assert_component_has_method(self.manager, 'critical')


class TestClipboardManagerInterface(ComponentTest):
    """剪贴板管理器接口测试"""

    def setUp(self):
        """测试前准备"""
        self.manager = ClipboardManager()

    def test_clipboard_manager_has_copy_text_method(self):
        """测试剪贴板管理器有复制文本方法"""
        self.assert_component_has_method(self.manager, 'copy_text')

    def test_clipboard_manager_has_get_text_method(self):
        """测试剪贴板管理器有获取文本方法"""
        self.assert_component_has_method(self.manager, 'get_text')

    def test_clipboard_manager_has_clear_method(self):
        """测试剪贴板管理器有清除方法"""
        self.assert_component_has_method(self.manager, 'clear')


class TestIconProviderInterface(ComponentTest):
    """图标提供器接口测试"""

    def setUp(self):
        """测试前准备"""
        self.provider = IconProvider()

    def test_icon_provider_has_get_file_icon_method(self):
        """测试图标提供器有获取文件图标方法"""
        self.assert_component_has_method(self.provider, 'get_file_icon')

    def test_icon_provider_has_get_folder_icon_method(self):
        """测试图标提供器有获取文件夹图标方法"""
        self.assert_component_has_method(self.provider, 'get_folder_icon')


class TestFileSystemHelperInterface(ComponentTest):
    """文件系统辅助工具接口测试"""

    def setUp(self):
        """测试前准备"""
        self.helper = FileSystemHelper()

    def test_file_system_helper_has_get_file_info_method(self):
        """测试文件系统辅助工具有获取文件信息方法"""
        self.assert_component_has_method(self.helper, 'get_file_info')

    def test_file_system_helper_has_get_folder_info_method(self):
        """测试文件系统辅助工具有获取文件夹信息方法"""
        self.assert_component_has_method(self.helper, 'get_folder_info')

    def test_file_system_helper_has_get_disk_usage_method(self):
        """测试文件系统辅助工具有获取磁盘使用方法"""
        self.assert_component_has_method(self.helper, 'get_disk_usage')


class TestTreeLoaderInterface(ComponentTest):
    """树形结构加载器接口测试"""

    def setUp(self):
        """测试前准备"""
        self.loader = TreeLoader()

    def test_tree_loader_has_load_tree_method(self):
        """测试树形结构加载器有加载树方法"""
        self.assert_component_has_method(self.loader, 'load_tree')

    def test_tree_loader_has_load_children_method(self):
        """测试树形结构加载器有加载子节点方法"""
        self.assert_component_has_method(self.loader, 'load_children')

    def test_tree_loader_has_has_children_method(self):
        """测试树形结构加载器有判断是否有子节点方法"""
        self.assert_component_has_method(self.loader, 'has_children')


class TestCommandInterfaces(ComponentTest):
    """命令接口测试"""

    def test_base_command_has_execute_method(self):
        """测试命令基类有执行方法"""
        self.assertTrue(hasattr(BaseCommand, 'execute'))

    def test_base_command_has_undo_method(self):
        """测试命令基类有撤销方法"""
        self.assertTrue(hasattr(BaseCommand, 'undo'))

    def test_base_command_has_redo_method(self):
        """测试命令基类有重做方法"""
        self.assertTrue(hasattr(BaseCommand, 'redo'))

    def test_copy_command_exists(self):
        """测试复制命令存在"""
        self.assertIsNotNone(CopyCommand)

    def test_move_command_exists(self):
        """测试移动命令存在"""
        self.assertIsNotNone(MoveCommand)

    def test_delete_command_exists(self):
        """测试删除命令存在"""
        self.assertIsNotNone(DeleteCommand)

    def test_rename_command_exists(self):
        """测试重命名命令存在"""
        self.assertIsNotNone(RenameCommand)

    def test_command_invoker_has_execute_command_method(self):
        """测试命令调用器有执行命令方法"""
        invoker = CommandInvoker()
        self.assert_component_has_method(invoker, 'execute_command')

    def test_command_invoker_has_undo_method(self):
        """测试命令调用器有撤销方法"""
        invoker = CommandInvoker()
        self.assert_component_has_method(invoker, 'undo')

    def test_command_invoker_has_redo_method(self):
        """测试命令调用器有重做方法"""
        invoker = CommandInvoker()
        self.assert_component_has_method(invoker, 'redo')


class TestSignalInterfaces(ComponentTest):
    """信号接口测试"""

    def test_sidebar_signals_has_node_expanded_signal(self):
        """测试侧边栏信号有节点展开信号"""
        self.assert_component_has_attribute(SidebarSignals, 'node_expanded')

    def test_sidebar_signals_has_node_collapsed_signal(self):
        """测试侧边栏信号有节点收起信号"""
        self.assert_component_has_attribute(SidebarSignals, 'node_collapsed')

    def test_sidebar_signals_has_node_selected_signal(self):
        """测试侧边栏信号有节点选择信号"""
        self.assert_component_has_attribute(SidebarSignals, 'node_selected')

    def test_file_manager_signals_has_file_selected_signal(self):
        """测试文件管理区信号有文件选择信号"""
        self.assert_component_has_attribute(FileManagerSignals, 'file_selected')

    def test_file_manager_signals_has_file_double_clicked_signal(self):
        """测试文件管理区信号有文件双击信号"""
        self.assert_component_has_attribute(FileManagerSignals, 'file_double_clicked')

    def test_preview_signals_has_preview_loaded_signal(self):
        """测试预览信号有预览加载信号"""
        self.assert_component_has_attribute(PreviewSignals, 'preview_loaded')

    def test_preview_signals_has_preview_failed_signal(self):
        """测试预览信号有预览失败信号"""
        self.assert_component_has_attribute(PreviewSignals, 'preview_failed')

    def test_file_operation_signals_has_operation_started_signal(self):
        """测试文件操作信号有操作开始信号"""
        self.assert_component_has_attribute(FileOperationSignals, 'operation_started')

    def test_file_operation_signals_has_operation_finished_signal(self):
        """测试文件操作信号有操作完成信号"""
        self.assert_component_has_attribute(FileOperationSignals, 'operation_finished')

    def test_main_window_signals_has_sidebar_selected_signal(self):
        """测试主窗口信号有侧边栏选择信号"""
        self.assert_component_has_attribute(MainWindowSignals, 'sidebar_selected')


class TestValidatorInterfaces(ComponentTest):
    """验证器接口测试"""

    def test_file_validator_has_validate_path_method(self):
        """测试文件验证器有验证路径方法"""
        validator = FileValidator()
        self.assert_component_has_method(validator, 'validate_path')

    def test_file_validator_has_validate_name_method(self):
        """测试文件验证器有验证名称方法"""
        validator = FileValidator()
        self.assert_component_has_method(validator, 'validate_name')

    def test_folder_validator_has_validate_path_method(self):
        """测试文件夹验证器有验证路径方法"""
        validator = FolderValidator()
        self.assert_component_has_method(validator, 'validate_path')

    def test_folder_validator_has_validate_name_method(self):
        """测试文件夹验证器有验证名称方法"""
        validator = FolderValidator()
        self.assert_component_has_method(validator, 'validate_name')

    def test_config_validator_has_validate_method(self):
        """测试配置验证器有验证方法"""
        validator = ConfigValidator()
        self.assert_component_has_method(validator, 'validate')


if __name__ == '__main__':
    unittest.main()