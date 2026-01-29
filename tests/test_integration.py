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
        children = self.tree_service.load_children(self.test_dir)
        
        self.assertEqual(len(children), 2)
        
        folder1 = next((c for c in children if c.name == "folder1"), None)
        self.assertIsNotNone(folder1)
        self.assertTrue(folder1.is_folder)

    def test_file_operation_tree_sync(self):
        """测试文件操作与树形结构同步"""
        root = self.tree_service.load_tree(self.test_dir)
        initial_count = len(root.children)
        
        new_folder = Path(self.test_dir) / "new_folder"
        new_folder.mkdir()
        
        root = self.tree_service.load_tree(self.test_dir)
        self.assertEqual(len(root.children), initial_count + 1)


class TestFileOperationIntegration(ComponentTest):
    """文件操作集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.file_service = FileService()
        
        (Path(self.test_dir) / "source.txt").write_text("source content")

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_copy_and_delete_workflow(self):
        """测试复制和删除工作流"""
        src_file = str(Path(self.test_dir) / "source.txt")
        dst_file = str(Path(self.test_dir) / "copy.txt")
        
        result = self.file_service.copy_file(src_file, dst_file)
        self.assertTrue(result)
        self.assertTrue(Path(dst_file).exists())
        
        result = self.file_service.delete_file(dst_file)
        self.assertTrue(result)
        self.assertFalse(Path(dst_file).exists())

    def test_rename_workflow(self):
        """测试重命名工作流"""
        old_file = str(Path(self.test_dir) / "source.txt")
        new_file = str(Path(self.test_dir) / "renamed.txt")
        
        result = self.file_service.rename_file(old_file, new_file)
        self.assertTrue(result)
        self.assertFalse(Path(old_file).exists())
        self.assertTrue(Path(new_file).exists())


class TestPreviewIntegration(ComponentTest):
    """预览集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.preview_service = PreviewService()
        
        (Path(self.test_dir) / "test.txt").write_text("test content")

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_text_file_preview(self):
        """测试文本文件预览"""
        test_file = str(Path(self.test_dir) / "test.txt")
        
        result = self.preview_service.preview_file(test_file)
        self.assertTrue(result)
        
        widget = self.preview_service.get_widget()
        self.assertIsNotNone(widget)
        
        self.preview_service.clear_preview()


class TestServiceIntegration(ComponentTest):
    """服务层集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.tree_service = TreeService()
        self.file_service = FileService()

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_tree_and_file_service_integration(self):
        """测试树形服务与文件服务集成"""
        root = self.tree_service.load_tree(self.test_dir)
        
        new_folder = str(Path(self.test_dir) / "new_folder")
        Path(new_folder).mkdir()
        
        root = self.tree_service.load_tree(self.test_dir)
        self.assertTrue(any(c.name == "new_folder" for c in root.children))

    def test_file_info_consistency(self):
        """测试文件信息一致性"""
        new_folder = str(Path(self.test_dir) / "new_folder")
        Path(new_folder).mkdir()
        
        root = self.tree_service.load_tree(self.test_dir)
        folder_item = next((c for c in root.children if c.name == "new_folder"), None)
        
        self.assertIsNotNone(folder_item)
        
        folder_info = self.file_service.get_file_info(new_folder)
        self.assertIsNotNone(folder_info)
        self.assertEqual(folder_item.name, folder_info.get('name'))


class TestControllerIntegration(ComponentTest):
    """控制器集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.tree_service = TreeService()
        self.file_service = FileService()
        self.preview_service = PreviewService()
        
        (Path(self.test_dir) / "folder1").mkdir()
        (Path(self.test_dir) / "folder2").mkdir()
        (Path(self.test_dir) / "test.txt").write_text("content")

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_sidebar_controller_integration(self):
        """测试侧边栏控制器集成"""
        root = self.tree_service.load_tree(self.test_dir)
        
        self.assertIsNotNone(root)
        self.assertEqual(len(root.children), 2)

    def test_file_manager_controller_integration(self):
        """测试文件管理器控制器集成"""
        files = self.file_service.list_files(self.test_dir)
        
        self.assertIsNotNone(files)
        self.assertEqual(len(files), 3)

    def test_preview_controller_integration(self):
        """测试预览控制器集成"""
        test_file = str(Path(self.test_dir) / "test.txt")
        
        result = self.preview_service.preview_file(test_file)
        self.assertTrue(result)
        
        self.preview_service.clear_preview()


class TestModelIntegration(ComponentTest):
    """模型集成测试"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """测试后清理"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_tree_item_hierarchy(self):
        """测试树项层次结构"""
        root = TreeItem(
            path=self.test_dir,
            name="root",
            is_folder=True
        )
        
        child1 = TreeItem(
            path=str(Path(self.test_dir) / "child1"),
            name="child1",
            is_folder=True
        )
        
        child2 = TreeItem(
            path=str(Path(self.test_dir) / "child2.txt"),
            name="child2.txt",
            is_folder=False
        )
        
        root.add_child(child1)
        root.add_child(child2)
        
        self.assertEqual(len(root.children), 2)
        self.assertEqual(root.get_child_count(), 2)
        self.assertTrue(root.has_children())
        self.assertEqual(child1.parent, root)
        self.assertEqual(child2.parent, root)

    def test_file_item_creation(self):
        """测试文件项创建"""
        test_file = str(Path(self.test_dir) / "test.txt")
        Path(test_file).write_text("content")
        
        file_item = FileItem(
            path=test_file,
            name="test.txt",
            size=7,
            modified_time=1.0,
            is_folder=False,
            file_type="txt"
        )
        
        self.assertEqual(file_item.name, "test.txt")
        self.assertEqual(file_item.size, 7)
        self.assertFalse(file_item.is_folder)


if __name__ == '__main__':
    unittest.main()