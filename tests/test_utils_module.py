import unittest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from tests.test_base import ComponentTest
from utils.path_helper import PathHelper
from utils.datetime_helper import DateTimeHelper
from utils.string_helper import StringHelper
from utils.file_sorter import FileSorter, SortColumn, SortOrder
from utils.file_filter import FileFilter, FilterType
from utils.preview_zoomer import PreviewZoomer
from models.file_item import FileItem
from models.tree_item import TreeItem
from datetime import datetime
from PySide6.QtWidgets import QApplication

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)


class TestPathHelper(ComponentTest):
    """路径辅助工具测试"""

    def test_normalize(self):
        """测试路径规范化"""
        path = "C:/Users/Test/../Documents"
        normalized = PathHelper.normalize(path)
        self.assertIn("Documents", normalized)

    def test_join(self):
        """测试路径连接"""
        path = PathHelper.join("C:", "Users", "Documents")
        self.assertIn("Users", path)
        self.assertIn("Documents", path)

    def test_get_basename(self):
        """测试获取文件名"""
        path = "C:/Users/Documents/test.txt"
        basename = PathHelper.get_basename(path)
        self.assertEqual(basename, "test.txt")

    def test_get_extension(self):
        """测试获取扩展名"""
        path = "C:/Users/Documents/test.txt"
        extension = PathHelper.get_extension(path)
        self.assertEqual(extension, ".txt")

    def test_is_absolute(self):
        """测试判断绝对路径"""
        self.assertTrue(PathHelper.is_absolute("C:/Users/Documents"))
        self.assertFalse(PathHelper.is_absolute("Documents"))

    def test_exists(self):
        """测试判断路径存在"""
        self.assertTrue(PathHelper.exists("C:/Users"))
        self.assertFalse(PathHelper.exists("C:/NonExistentPath"))

    def test_path_helper_docstring(self):
        """测试路径辅助工具文档字符串"""
        self.assert_component_docstring(PathHelper)


class TestDateTimeHelper(ComponentTest):
    """日期时间辅助工具测试"""

    def test_now(self):
        """测试获取当前时间"""
        now = DateTimeHelper.now()
        self.assertIsInstance(now, datetime)

    def test_format(self):
        """测试格式化时间"""
        dt = datetime(2026, 1, 29, 12, 30, 45)
        formatted = DateTimeHelper.format(dt, "%Y-%m-%d %H:%M:%S")
        self.assertEqual(formatted, "2026-01-29 12:30:45")

    def test_format_size(self):
        """测试格式化大小"""
        size = DateTimeHelper.format_size(1024)
        self.assertIn("KB", size)

        size = DateTimeHelper.format_size(1024 * 1024)
        self.assertIn("MB", size)

    def test_format_file_time(self):
        """测试格式化文件时间"""
        now = DateTimeHelper.now()
        formatted = DateTimeHelper.format_file_time(now.timestamp())
        self.assertIn("刚刚", formatted)

    def test_datetime_helper_docstring(self):
        """测试日期时间辅助工具文档字符串"""
        self.assert_component_docstring(DateTimeHelper)


class TestStringHelper(ComponentTest):
    """字符串辅助工具测试"""

    def test_is_empty(self):
        """测试判断字符串为空"""
        self.assertTrue(StringHelper.is_empty(""))
        self.assertTrue(StringHelper.is_empty("   "))
        self.assertFalse(StringHelper.is_empty("test"))

    def test_trim(self):
        """测试去除首尾空格"""
        s = "  test  "
        trimmed = StringHelper.trim(s)
        self.assertEqual(trimmed, "test")

    def test_to_lower(self):
        """测试转换为小写"""
        s = "TEST"
        lower = StringHelper.to_lower(s)
        self.assertEqual(lower, "test")

    def test_to_upper(self):
        """测试转换为大写"""
        s = "test"
        upper = StringHelper.to_upper(s)
        self.assertEqual(upper, "TEST")

    def test_contains(self):
        """测试判断包含子串"""
        s = "Hello World"
        self.assertTrue(StringHelper.contains(s, "world"))
        self.assertFalse(StringHelper.contains(s, "python"))

    def test_split(self):
        """测试分割字符串"""
        s = "a,b,c"
        parts = StringHelper.split(s, ",")
        self.assertEqual(len(parts), 3)

    def test_join(self):
        """测试连接字符串"""
        parts = ["a", "b", "c"]
        joined = StringHelper.join(parts, ",")
        self.assertEqual(joined, "a,b,c")

    def test_replace(self):
        """测试替换字符串"""
        s = "Hello World"
        replaced = StringHelper.replace(s, "World", "Python")
        self.assertEqual(replaced, "Hello Python")

    def test_string_helper_docstring(self):
        """测试字符串辅助工具文档字符串"""
        self.assert_component_docstring(StringHelper)


class TestFileSorter(ComponentTest):
    """文件排序工具测试"""

    def setUp(self):
        """测试前准备"""
        self.sorter = FileSorter()
        self.files = [
            FileItem(path="/test/b.txt", name="b.txt", size=100, modified_time=1.0, is_folder=False, file_type="txt"),
            FileItem(path="/test/a.txt", name="a.txt", size=200, modified_time=2.0, is_folder=False, file_type="txt"),
            FileItem(path="/test/c.txt", name="c.txt", size=150, modified_time=1.5, is_folder=False, file_type="txt")
        ]

    def test_sort_by_name(self):
        """测试按名称排序"""
        self.sorter.set_sort_column(SortColumn.NAME)
        self.sorter.set_sort_order(SortOrder.ASCENDING)
        sorted_files = self.sorter.sort(self.files)
        self.assertEqual(sorted_files[0].name, "a.txt")
        self.assertEqual(sorted_files[1].name, "b.txt")
        self.assertEqual(sorted_files[2].name, "c.txt")

    def test_sort_by_size(self):
        """测试按大小排序"""
        self.sorter.set_sort_column(SortColumn.SIZE)
        self.sorter.set_sort_order(SortOrder.ASCENDING)
        sorted_files = self.sorter.sort(self.files)
        self.assertEqual(sorted_files[0].size, 100)
        self.assertEqual(sorted_files[1].size, 150)
        self.assertEqual(sorted_files[2].size, 200)

    def test_file_sorter_docstring(self):
        """测试文件排序工具文档字符串"""
        self.assert_component_docstring(FileSorter)


class TestFileFilter(ComponentTest):
    """文件过滤工具测试"""

    def setUp(self):
        """测试前准备"""
        self.filter = FileFilter()
        self.files = [
            FileItem(path="/test/.hidden", name=".hidden", size=100, modified_time=1.0, is_folder=False, file_type="txt"),
            FileItem(path="/test/a.txt", name="a.txt", size=200, modified_time=2.0, is_folder=False, file_type="txt"),
            FileItem(path="/test/b.py", name="b.py", size=150, modified_time=1.5, is_folder=False, file_type="py")
        ]

    def test_filter_by_type(self):
        """测试按类型过滤"""
        self.filter.set_filter_type(FilterType.FILES_ONLY)
        filtered = self.filter.filter(self.files)
        self.assertEqual(len(filtered), 2)

    def test_filter_by_text(self):
        """测试按文本过滤"""
        self.filter.set_filter_text("a")
        filtered = self.filter.filter(self.files)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, "a.txt")

    def test_filter_by_hidden(self):
        """测试按隐藏文件过滤"""
        self.filter.set_show_hidden(False)
        filtered = self.filter.filter(self.files)
        self.assertEqual(len(filtered), 2)

    def test_filter_by_extension(self):
        """测试按扩展名过滤"""
        self.filter.set_extension_filter(".txt")
        filtered = self.filter.filter(self.files)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, "a.txt")

    def test_file_filter_docstring(self):
        """测试文件过滤工具文档字符串"""
        self.assert_component_docstring(FileFilter)


class TestPreviewZoomer(ComponentTest):
    """预览缩放工具测试"""

    def setUp(self):
        """测试前准备"""
        from PySide6.QtWidgets import QWidget
        self.widget = QWidget()
        self.zoomer = PreviewZoomer(self.widget)

    def test_zoom_in(self):
        """测试放大"""
        initial_zoom = self.zoomer.get_zoom_level()
        self.zoomer.zoom_in()
        new_zoom = self.zoomer.get_zoom_level()
        self.assertGreater(new_zoom, initial_zoom)

    def test_zoom_out(self):
        """测试缩小"""
        self.zoomer.set_zoom_level(2.0)
        initial_zoom = self.zoomer.get_zoom_level()
        self.zoomer.zoom_out()
        new_zoom = self.zoomer.get_zoom_level()
        self.assertLess(new_zoom, initial_zoom)

    def test_reset_zoom(self):
        """测试重置缩放"""
        self.zoomer.set_zoom_level(2.0)
        self.zoomer.reset_zoom()
        zoom_level = self.zoomer.get_zoom_level()
        self.assertEqual(zoom_level, 1.0)

    def test_set_zoom_level(self):
        """测试设置缩放级别"""
        self.zoomer.set_zoom_level(2.5)
        zoom_level = self.zoomer.get_zoom_level()
        self.assertEqual(zoom_level, 2.5)

    def test_get_zoom_percentage(self):
        """测试获取缩放百分比"""
        self.zoomer.set_zoom_level(1.5)
        percentage = self.zoomer.get_zoom_percentage()
        self.assertEqual(percentage, 150)

    def test_preview_zoomer_docstring(self):
        """测试预览缩放工具文档字符串"""
        self.assert_component_docstring(PreviewZoomer)


class TestTreeItem(ComponentTest):
    """树项模型测试"""

    def test_tree_item_creation(self):
        """测试树项创建"""
        item = TreeItem(path="/test", name="test", is_folder=True)
        self.assertEqual(item.path, "/test")
        self.assertEqual(item.name, "test")
        self.assertTrue(item.is_folder)

    def test_tree_item_add_child(self):
        """测试添加子节点"""
        parent = TreeItem(path="/parent", name="parent", is_folder=True)
        child = TreeItem(path="/parent/child", name="child", is_folder=True)
        parent.add_child(child)
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0].name, "child")

    def test_tree_item_remove_child(self):
        """测试移除子节点"""
        parent = TreeItem(path="/parent", name="parent", is_folder=True)
        child = TreeItem(path="/parent/child", name="child", is_folder=True)
        parent.add_child(child)
        parent.remove_child(child)
        self.assertEqual(len(parent.children), 0)

    def test_tree_item_docstring(self):
        """测试树项文档字符串"""
        self.assert_component_docstring(TreeItem)


if __name__ == '__main__':
    unittest.main()