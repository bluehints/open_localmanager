import unittest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from tests.test_config_module import TestConfigModule
from tests.test_utils_module import (
    TestPathHelper,
    TestDateTimeHelper,
    TestStringHelper,
    TestFileSorter,
    TestFileFilter,
    TestPreviewZoomer,
    TestTreeItem
)
from tests.test_interfaces import (
    TestFileServiceInterface,
    TestFolderServiceInterface,
    TestTreeServiceInterface,
    TestPreviewServiceInterface,
    TestConfigManagerInterface,
    TestLogManagerInterface,
    TestClipboardManagerInterface,
    TestIconProviderInterface,
    TestFileSystemHelperInterface,
    TestTreeLoaderInterface,
    TestCommandInterfaces,
    TestSignalInterfaces,
    TestValidatorInterfaces
)
from tests.test_integration import (
    TestSidebarFileManagerSync,
    TestFileOperationIntegration,
    TestPreviewIntegration,
    TestServiceIntegration,
    TestControllerIntegration,
    TestModelIntegration
)


def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("Open资料助手 - 组件测试套件")
    print("="*60)
    print()

    test_suites = [
        ("配置模块测试", TestConfigModule),
        ("路径辅助工具测试", TestPathHelper),
        ("日期时间辅助工具测试", TestDateTimeHelper),
        ("字符串辅助工具测试", TestStringHelper),
        ("文件排序工具测试", TestFileSorter),
        ("文件过滤工具测试", TestFileFilter),
        ("预览缩放工具测试", TestPreviewZoomer),
        ("树项模型测试", TestTreeItem),
        ("文件服务接口测试", TestFileServiceInterface),
        ("文件夹服务接口测试", TestFolderServiceInterface),
        ("树形结构服务接口测试", TestTreeServiceInterface),
        ("预览服务接口测试", TestPreviewServiceInterface),
        ("配置管理器接口测试", TestConfigManagerInterface),
        ("日志管理器接口测试", TestLogManagerInterface),
        ("剪贴板管理器接口测试", TestClipboardManagerInterface),
        ("图标提供器接口测试", TestIconProviderInterface),
        ("文件系统辅助工具接口测试", TestFileSystemHelperInterface),
        ("树形结构加载器接口测试", TestTreeLoaderInterface),
        ("命令接口测试", TestCommandInterfaces),
        ("信号接口测试", TestSignalInterfaces),
        ("验证器接口测试", TestValidatorInterfaces),
        ("侧边栏与文件管理区同步测试", TestSidebarFileManagerSync),
        ("文件操作集成测试", TestFileOperationIntegration),
        ("预览集成测试", TestPreviewIntegration),
        ("服务层集成测试", TestServiceIntegration),
        ("控制器集成测试", TestControllerIntegration),
        ("模型集成测试", TestModelIntegration)
    ]

    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_errors = 0

    for suite_name, test_class in test_suites:
        print(f"\n运行测试套件: {suite_name}")
        print("-" * 60)

        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=1)
        result = runner.run(suite)

        total_tests += result.testsRun
        total_passed += result.testsRun - len(result.failures) - len(result.errors)
        total_failed += len(result.failures)
        total_errors += len(result.errors)

        if len(result.failures) == 0 and len(result.errors) == 0:
            print(f"✓ {suite_name} - 全部通过")
        else:
            print(f"✗ {suite_name} - 失败: {len(result.failures)}, 错误: {len(result.errors)}")

    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"总测试数: {total_tests}")
    print(f"通过: {total_passed}")
    print(f"失败: {total_failed}")
    print(f"错误: {total_errors}")
    print(f"通过率: {(total_passed/total_tests*100):.2f}%")

    if total_failed == 0 and total_errors == 0:
        print("\n" + "="*60)
        print("✓ 所有测试通过！")
        print("="*60)
        return True
    else:
        print("\n" + "="*60)
        print("✗ 有测试失败或错误！")
        print("="*60)
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)