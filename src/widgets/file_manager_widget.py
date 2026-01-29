from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QHeaderView
)
from PySide6.QtCore import Qt, QPoint
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from signals.file_manager_signals import FileManagerSignals
from models.file_table_model import FileTableModel
from models.file_sort_filter_proxy_model import FileSortFilterProxyModel
from widgets.file_list_delegate import FileListDelegate


class FileManagerWidget(QWidget):
    """文件管理区组件"""

    def __init__(self, parent=None):
        """
        初始化文件管理区

        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self.signals = FileManagerSignals()
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.setSortingEnabled(True)

        self.table_model = FileTableModel()
        self.proxy_model = FileSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.table_model)
        self.table_view.setModel(self.proxy_model)

        delegate = FileListDelegate()
        self.table_view.setItemDelegate(delegate)

        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        layout.addWidget(self.table_view)

    def _setup_connections(self):
        """建立信号槽连接"""
        self.table_view.clicked.connect(self._on_item_clicked)
        self.table_view.doubleClicked.connect(self._on_item_double_clicked)
        self.table_view.customContextMenuRequested.connect(self._on_context_menu)

    def _on_item_clicked(self, index):
        """
        处理文件点击事件

        Args:
            index: 模型索引
        """
        source_index = self.proxy_model.mapToSource(index)
        file_item = self.table_model.get_file(source_index)
        if file_item:
            self.signals.file_selected.emit(file_item.path)

    def _on_item_double_clicked(self, index):
        """
        处理文件双击事件

        Args:
            index: 模型索引
        """
        source_index = self.proxy_model.mapToSource(index)
        file_item = self.table_model.get_file(source_index)
        if file_item:
            self.signals.file_double_clicked.emit(file_item.path)

    def _on_context_menu(self, position: QPoint):
        """
        处理右键菜单事件

        Args:
            position: 位置
        """
        index = self.table_view.indexAt(position)
        if index.isValid():
            source_index = self.proxy_model.mapToSource(index)
            file_item = self.table_model.get_file(source_index)
            if file_item:
                global_position = self.table_view.mapToGlobal(position)
                self.signals.context_menu_requested.emit(file_item.path, global_position)

    def load_files(self, files):
        """
        加载文件列表

        Args:
            files: 文件列表
        """
        self.table_model.refresh(files)

    def select_file(self, file_path: str):
        """
        选中文件

        Args:
            file_path: 文件路径
        """
        for row in range(self.table_model.rowCount()):
            index = self.table_model.index(row, 0)
            file_item = self.table_model.get_file(index)
            if file_item and file_item.path == file_path:
                proxy_index = self.proxy_model.mapFromSource(index)
                self.table_view.selectRow(proxy_index.row())
                break

    def refresh_files(self):
        """刷新文件列表"""
        pass

    def set_filter_text(self, text: str):
        """
        设置过滤文本

        Args:
            text: 过滤文本
        """
        self.proxy_model.set_filter_text(text)

    def set_show_hidden(self, show: bool):
        """
        设置是否显示隐藏文件

        Args:
            show: 是否显示
        """
        self.proxy_model.set_show_hidden(show)

    def set_sort_column(self, column: int):
        """
        设置排序列

        Args:
            column: 列号
        """
        self.table_view.sortByColumn(column, self.proxy_model.sortOrder())

    def set_sort_order(self, order: Qt.SortOrder):
        """
        设置排序顺序

        Args:
            order: 排序顺序
        """
        self.table_view.sortByColumn(self.proxy_model.sortColumn(), order)