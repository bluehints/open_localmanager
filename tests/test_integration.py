import unittest
import sys
import tempfile
import shutil
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from tests.test_base import ComponentTest
from controllers.sidebar_controller import SidebarController
from controllers.file_manager_controller import FileManagerController
from controllers.preview_controller import PreviewController
from services.tree_service import TreeService
from services.file_service import FileService
from services.preview_service import PreviewService
from models.tree_item import TreeItem
from models.file_item import FileItem


class TestSidebarFileManagerSync(ComponentTest):
    """侧边栏与文件管理区同步测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.tree_service = TreeService()
        self.file_service = FileService()
        
        (Path(self.test_dir) / "folder1").mkdir()
        (Path(self.test_dir) / "folder1" / "file1.txt").write_text("content1")
        (Path(self.test_dir) / "folder2").mkdir()
        (Path(self.test_dir) / "file2.txt").write_text("content2")

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_tree_load_structure(self):
        """测试树形结构加载"""
        root = self.tree_service.load_tree(self.test_dir)
        
        self.assertIsNotNone(root)
        self.assertTrue(root.is_folder)
        self.assertEqual(len(root.children), 2)

    def test_tree_folder_expansion(self):
        """测试文件夹展开"""
        root = self.tree_service.load_tree(self.test_dir)
        
        folder1 = root.children[0]
        self.assertFalse(folder1.is_expanded)
        
        folder1.is_expanded = True
        children = self.tree_service.load_children(folder1.path)
        
        self.assertEqual(len(children), 1)

    def test_file_manager_sync(self):
        """测试文件管理区同步"""
        root = self.tree_service.load_tree(self.test_dir)
        folder1 = root.children[0]
        
        files = self.file_service.list_files(folder1.path)
        
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "file1.txt")


class TestFileOperationIntegration(ComponentTest):
    """文件操作集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.file_service = FileService()
        
        (Path(self.test_dir) / "test.txt").write_text("test content")

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_copy_file(self):
        """测试复制文件"""
        src_path = str(Path(self.test_dir) / "test.txt")
        dst_path = str(Path(self.test_dir) / "test_copy.txt")
        
        result = self.file_service.copy_file(src_path, dst_path)
        
        self.assertTrue(result)
        self.assertTrue(Path(dst_path).exists())

    def test_delete_file(self):
        """测试删除文件"""
        file_path = str(Path(self.test_dir) / "test.txt")
        
        result = self.file_service.delete_file(file_path)
        
        self.assertTrue(result)
        self.assertFalse(Path(file_path).exists())


class TestPreviewIntegration(ComponentTest):
    """预览集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        
        (Path(self.test_dir) / "test.txt").write_text("test content")

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_text_preview(self):
        """测试文本预览"""
        from PySide6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        preview_service = PreviewService()
        file_path = str(Path(self.test_dir) / "test.txt")
        
        result = preview_service.preview_file(file_path)
        
        self.assertTrue(result)


class TestServiceIntegration(ComponentTest):
    """服务层集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.tree_service = TreeService()
        self.file_service = FileService()
        
        (Path(self.test_dir) / "folder1").mkdir()
        (Path(self.test_dir) / "folder1" / "file1.txt").write_text("content1")

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_file_info_consistency(self):
        """测试文件信息一致性"""
        file_path = str(Path(self.test_dir) / "folder1" / "file1.txt")
        
        file_info = self.file_service.get_file_info(file_path)
        
        self.assertEqual(file_info['name'], "file1.txt")
        self.assertEqual(file_info['is_folder'], False)
        self.assertGreater(file_info['size'], 0)

    def test_folder_listing(self):
        """测试文件夹列表"""
        files = self.file_service.list_files(self.test_dir)
        
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "folder1")
        self.assertTrue(files[0].is_folder)


class TestControllerIntegration(ComponentTest):
    """控制器集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        
        (Path(self.test_dir) / "folder1").mkdir()
        (Path(self.test_dir) / "folder1" / "file1.txt").write_text("content1")
        (Path(self.test_dir) / "file2.txt").write_text("content2")

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_sidebar_controller(self):
        """测试侧边栏控制器"""
        from PySide6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        controller = SidebarController()
        controller.load_tree(self.test_dir)
        
        self.assertIsNotNone(controller.get_root_item())

    def test_file_manager_controller_integration(self):
        """测试文件管理区控制器集成"""
        from PySide6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        controller = FileManagerController()
        controller.load_files(self.test_dir)
        
        files = controller.get_files()
        self.assertGreater(len(files), 0)

    def test_preview_controller_integration(self):
        """测试预览控制器集成"""
        from PySide6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        controller = PreviewController()
        file_path = str(Path(self.test_dir) / "file2.txt")
        
        result = controller.preview_file(file_path)
        
        self.assertTrue(result)


class TestModelIntegration(ComponentTest):
    """模型集成测试"""

    def test_tree_item_hierarchy(self):
        """测试树项层级关系"""
        root = TreeItem(path="/root", name="root", is_folder=True)
        child1 = TreeItem(path="/root/child1", name="child1", is_folder=True)
        child2 = TreeItem(path="/root/child2", name="child2", is_folder=False)
        
        root.add_child(child1)
        root.add_child(child2)
        
        self.assertEqual(root.get_child_count(), 2)
        self.assertEqual(child1.parent, root)
        self.assertEqual(child2.parent, root)
        self.assertEqual(child1.get_row(), 0)
        self.assertEqual(child2.get_row(), 1)

    def test_file_item_properties(self):
        """测试文件项属性"""
        from datetime import datetime
        
        file_item = FileItem(
            path="/test/file.txt",
            name="file.txt",
            size=1024,
            modified_time=datetime.now(),
            is_folder=False,
            file_type=".txt"
        )
        
        self.assertEqual(file_item.name, "file.txt")
        self.assertEqual(file_item.size, 1024)
        self.assertFalse(file_item.is_folder)
        self.assertEqual(file_item.file_type, ".txt")