from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QToolButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QAction


class SearchBox(QWidget):
    """搜索框组件"""

    search_changed = Signal(str)
    search_cleared = Signal()

    def __init__(self, parent=None):
        """
        初始化搜索框

        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """设置用户界面"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText("搜索文件...")
        self._search_edit.setClearButtonEnabled(True)
        self._search_edit.setMinimumWidth(200)
        layout.addWidget(self._search_edit)

        self._search_button = QPushButton("搜索")
        self._search_button.setMinimumWidth(60)
        layout.addWidget(self._search_button)

        self._clear_button = QPushButton("清除")
        self._clear_button.setMinimumWidth(60)
        self._clear_button.setVisible(False)
        layout.addWidget(self._clear_button)

    def _setup_connections(self):
        """建立信号槽连接"""
        self._search_edit.textChanged.connect(self._on_text_changed)
        self._search_edit.returnPressed.connect(self._on_search)
        self._search_button.clicked.connect(self._on_search)
        self._clear_button.clicked.connect(self._on_clear)

    def _on_text_changed(self, text: str):
        """
        处理文本变化事件

        Args:
            text: 文本
        """
        has_text = bool(text.strip())
        self._clear_button.setVisible(has_text)
        self.search_changed.emit(text)

    def _on_search(self):
        """处理搜索事件"""
        text = self._search_edit.text().strip()
        if text:
            self.search_changed.emit(text)

    def _on_clear(self):
        """处理清除事件"""
        self._search_edit.clear()
        self._clear_button.setVisible(False)
        self.search_cleared.emit()

    def get_search_text(self) -> str:
        """
        获取搜索文本

        Returns:
            搜索文本
        """
        return self._search_edit.text().strip()

    def set_search_text(self, text: str):
        """
        设置搜索文本

        Args:
            text: 搜索文本
        """
        self._search_edit.setText(text)

    def clear(self):
        """清除搜索框"""
        self._on_clear()

    def set_placeholder(self, text: str):
        """
        设置占位符文本

        Args:
            text: 占位符文本
        """
        self._search_edit.setPlaceholderText(text)

    def set_focus(self):
        """设置焦点到搜索框"""
        self._search_edit.setFocus()
        self._search_edit.selectAll()