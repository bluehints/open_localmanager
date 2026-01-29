from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QMenu
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from signals.sidebar_signals import SidebarSignals
from utils.icon_provider import IconProvider


class SidebarWidget(QWidget):
    """结构树侧边栏组件"""

    def __init__(self, parent=None):
        """
        初始化侧边栏

        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self.signals = SidebarSignals()
        self.icon_provider = IconProvider()
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setEditTriggers(QTreeWidget.NoEditTriggers)
        self.tree_widget.setExpandsOnDoubleClick(False)
        self.tree_widget.setIndentation(15)
        self.tree_widget.setUniformRowHeights(True)
        self.tree_widget.setAnimated(True)
        layout.addWidget(self.tree_widget)

    def _setup_connections(self):
        """建立信号槽连接"""
        self.tree_widget.itemExpanded.connect(self._on_item_expanded)
        self.tree_widget.itemCollapsed.connect(self._on_item_collapsed)
        self.tree_widget.itemClicked.connect(self._on_item_clicked)
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self._on_context_menu)

    def _on_item_expanded(self, item: QTreeWidgetItem):
        """
        处理节点展开事件


        Args:
            item: 树项
        """
        path = item.data(0, Qt.UserRole)
        
        child_count = item.childCount()
        if child_count > 0:
            first_child = item.child(0)
            if first_child.text(0) == "+":
                item.removeChild(first_child)
                self._load_children(item, path)
        
        self.signals.node_expanded.emit(path)

    def _on_item_collapsed(self, item: QTreeWidgetItem):
        """
        处理节点收起事件


        Args:
            item: 树项
        """
        path = item.data(0, Qt.UserRole)
        self.signals.node_collapsed.emit(path)

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """
        处理节点点击事件


        Args:
            item: 树项
            column: 列号
        """
        path = item.data(0, Qt.UserRole)
        self.signals.node_selected.emit(path)

    def _on_context_menu(self, position: QPoint):
        """
        处理右键菜单事件

        Args:
            position: 位置
        """
        item = self.tree_widget.itemAt(position)
        if item:
            path = item.data(0, Qt.UserRole)
            self.signals.context_menu_requested.emit(path, position)

    def load_tree(self, root_path: str):
        """
        加载树形结构

        Args:
            root_path: 根路径
        """
        self.tree_widget.clear()
        
        if not os.path.exists(root_path):
            return

        root_item = QTreeWidgetItem(self.tree_widget)
        root_item.setText(0, os.path.basename(root_path) or root_path)
        root_item.setData(0, Qt.UserRole, root_path)
        root_item.setIcon(0, self.icon_provider.get_folder_icon())
        root_item.setExpanded(True)

        self._load_children(root_item, root_path)

    def _load_children(self, parent_item: QTreeWidgetItem, parent_path: str):
        """
        加载子节点

        Args:
            parent_item: 父节点
            parent_path: 父路径
        """
        try:
            entries = os.listdir(parent_path)
            entries.sort()

            for entry in entries:
                entry_path = os.path.join(parent_path, entry)
                
                if os.path.isdir(entry_path):
                    child_item = QTreeWidgetItem(parent_item)
                    child_item.setText(0, entry)
                    child_item.setData(0, Qt.UserRole, entry_path)
                    child_item.setIcon(0, self.icon_provider.get_folder_icon())

                    has_children = False
                    try:
                        sub_entries = os.listdir(entry_path)
                        for sub_entry in sub_entries:
                            if os.path.isdir(os.path.join(entry_path, sub_entry)):
                                has_children = True
                                break
                    except Exception:
                        pass

                    if has_children:
                        placeholder_item = QTreeWidgetItem(child_item)
                        placeholder_item.setText(0, "+")

        except Exception:
            pass

    def select_node(self, path: str):
        """
        选中节点

        Args:
            path: 路径
        """
        items = self.tree_widget.findItems(path, Qt.MatchExactly | Qt.MatchRecursive, 0)
        if items:
            self.tree_widget.setCurrentItem(items[0])

    def refresh_tree(self):
        """刷新树形结构"""
        pass