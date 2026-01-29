import os
from typing import Optional
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PySide6.QtGui import QFont, QTextOption
from .base_previewer import BasePreviewer


class TextPreviewer(BasePreviewer):
    """文本预览器"""

    TEXT_EXTENSIONS = {
        '.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml',
        '.yaml', '.yml', '.ini', '.cfg', '.conf', '.log', '.csv',
        '.sql', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.php',
        '.rb', '.go', '.rs', '.swift', '.kt', '.ts', '.tsx', '.jsx',
        '.vue', '.scss', '.sass', '.less', '.bat', '.sh', '.ps1'
    }

    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化文本预览器

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        self.widget = QWidget(self.parent)
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit = QTextEdit(self.widget)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text_edit.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        font = QFont("Consolas", 10)
        self.text_edit.setFont(font)

        layout.addWidget(self.text_edit)

    def can_preview(self, file_path: str) -> bool:
        """
        判断是否可以预览该文件

        Args:
            file_path: 文件路径

        Returns:
            是否可以预览
        """
        if not os.path.isfile(file_path):
            return False

        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.TEXT_EXTENSIONS

    def preview(self, file_path: str) -> bool:
        """
        预览文件

        Args:
            file_path: 文件路径

        Returns:
            预览是否成功
        """
        try:
            if not self.can_preview(file_path):
                return False

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            self.text_edit.setPlainText(content)
            self.current_path = file_path
            return True
        except Exception:
            return False

    def clear(self) -> None:
        """清空预览"""
        self.text_edit.clear()
        self.current_path = None

    def get_widget(self) -> QWidget:
        """
        获取预览窗口部件

        Returns:
            预览窗口部件
        """
        return self.widget