import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


class ComponentTest(unittest.TestCase):
    """组件测试基类"""

    def setUp(self):
        """测试前准备"""
        pass

    def tearDown(self):
        """测试后清理"""
        pass

    def assert_component_exists(self, module_path, component_name):
        """
        断言组件存在

        Args:
            module_path: 模块路径
            component_name: 组件名称
        """
        try:
            module = __import__(module_path, fromlist=[component_name])
            self.assertIsNotNone(getattr(module, component_name),
                           f"组件 {component_name} 不存在于模块 {module_path} 中")
        except ImportError as e:
            self.fail(f"无法导入模块 {module_path}: {e}")

    def assert_component_has_method(self, component, method_name):
        """
        断言组件有指定方法

        Args:
            component: 组件实例
            method_name: 方法名称
        """
        self.assertTrue(hasattr(component, method_name),
                       f"组件缺少方法: {method_name}")

    def assert_component_has_attribute(self, component, attribute_name):
        """
        断言组件有指定属性

        Args:
            component: 组件实例
            attribute_name: 属性名称
        """
        self.assertTrue(hasattr(component, attribute_name),
                       f"组件缺少属性: {attribute_name}")

    def assert_component_code_size(self, component_path, max_size=500):
        """
        断言组件代码量符合要求

        Args:
            component_path: 组件路径
            max_size: 最大代码行数
        """
        try:
            with open(component_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                code_lines = [line for line in lines
                             if line.strip() and not line.strip().startswith('#')]
                self.assertLessEqual(len(code_lines), max_size,
                                  f"组件代码量超过限制: {len(code_lines)} 行 > {max_size} 行")
        except Exception as e:
            self.fail(f"无法读取组件文件 {component_path}: {e}")

    def assert_component_imports(self, component_path, required_imports):
        """
        断言组件导入了必需的模块

        Args:
            component_path: 组件路径
            required_imports: 必需的导入列表
        """
        try:
            with open(component_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for imp in required_imports:
                    self.assertIn(imp, content,
                                f"组件缺少必需的导入: {imp}")
        except Exception as e:
            self.fail(f"无法读取组件文件 {component_path}: {e}")

    def assert_component_docstring(self, component):
        """
        断言组件有文档字符串

        Args:
            component: 组件实例或类
        """
        doc = component.__doc__
        self.assertIsNotNone(doc, f"组件缺少文档字符串")
        self.assertGreater(len(doc.strip()), 10, f"组件文档字符串过短")


class TestRunner:
    """测试运行器"""

    def __init__(self):
        """初始化测试运行器"""
        self.test_results = []
        self.passed = 0
        self.failed = 0
        self.errors = 0

    def run_test(self, test_class):
        """
        运行测试类

        Args:
            test_class: 测试类
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        self.test_results.append({
            'class': test_class.__name__,
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped)
        })

        self.passed += result.testsRun - len(result.failures) - len(result.errors)
        self.failed += len(result.failures)
        self.errors += len(result.errors)

    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "="*60)
        print("测试摘要")
        print("="*60)

        for result in self.test_results:
            print(f"\n测试类: {result['class']}")
            print(f"  运行测试: {result['tests_run']}")
            print(f"  失败: {result['failures']}")
            print(f"  错误: {result['errors']}")
            print(f"  跳过: {result['skipped']}")

        print("\n" + "="*60)
        print("总计")
        print("="*60)
        print(f"通过: {self.passed}")
        print(f"失败: {self.failed}")
        print(f"错误: {self.errors}")
        print(f"总计: {self.passed + self.failed + self.errors}")

        if self.failed == 0 and self.errors == 0:
            print("\n✓ 所有测试通过！")
        else:
            print("\n✗ 有测试失败或错误！")


if __name__ == '__main__':
    runner = TestRunner()
    runner.print_summary()