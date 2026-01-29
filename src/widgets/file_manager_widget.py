from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Qt, QPoint
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from signals.file_manager_signals import FileManagerSignals


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

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["名称", "大小", "修改时间", "类型"])
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)

        header = self.table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        layout.addWidget(self.table_widget)

    def _setup_connections(self):
        """建立信号槽连接"""
        self.table_widget.itemClicked.connect(self._on_item_clicked)
        self.table_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.table_widget.customContextMenuRequested.connect(self._on_context_menu)

    def _on_item_clicked(self, item: QTableWidgetItem):
        """
        处理文件点击事件

        Args:
            item: 表格项
        """
        row = item.row()
        file_path = self.table_widget.item(row, 0).data(Qt.UserRole)
        if file_path:
            self.signals.file_selected.emit(file_path)

    def _on_item_double_clicked(self, item: QTableWidgetItem):
        """
        处理文件双击事件

        Args:
            item: 表格项
        """
        row = item.row()
        file_path = self.table_widget.item(row, 0).data(Qt.UserRole)
        if file_path:
            self.signals.file_double_clicked.emit(file_path)

    def _on_context_menu(self, position: QPoint):
        """
        处理右键菜单事件

        Args:
            position: 位置
        """
        item = self.table_widget.itemAt(position)
        if item:
            row = item.row()
            file_path = self.table_widget.item(row, 0).data(Qt.UserRole)
            if file_path:
                global_position = self.table_widget.mapToGlobal(position)
                self.signals.context_menu_requested.emit(file_path, global_position)

    def load_files(self, files):
        """
        加载文件列表

        Args:
            files: 文件列表
        """
        self.table_widget.setRowCount(0)

        for file_info in files:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)

            name_item = QTableWidgetItem(file_info.name)
            name_item.setData(Qt.UserRole, file_info.path)
            self.table_widget.setItem(row, 0, name_item)

            size_item = QTableWidgetItem(file_info.get_size_str())
            size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table_widget.setItem(row, 1, size_item)

            time_item = QTableWidgetItem(file_info.get_modified_time_str())
            self.table_widget.setItem(row, 2, time_item)

            type_item = QTableWidgetItem(file_info.file_type)
            self.table_widget.setItem(row, 3, type_item)

    def select_file(self, file_path: str):
        """
        选中文件

        Args:
            file_path: 文件路径
        """
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 0)
            if item and item.data(Qt.UserRole) == file_path:
                self.table_widget.selectRow(row)
                break

    def refresh_files(self):
        """刷新文件列表"""
        pass