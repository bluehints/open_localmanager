from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QPushButton,
    QGroupBox,
    QLabel
)
from PySide6.QtCore import Qt, Signal
from typing import Optional


class FilterDialog(QDialog):
    """文件过滤对话框"""

    filter_applied = Signal(dict)

    def __init__(self, parent=None):
        """
        初始化文件过滤对话框

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.setWindowTitle("文件过滤")
        self.setMinimumWidth(400)
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)

        name_group = QGroupBox("名称过滤")
        name_layout = QFormLayout()

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("输入文件名或扩展名...")
        name_layout.addRow("文件名:", self._name_edit)

        name_group.setLayout(name_layout)
        layout.addWidget(name_group)

        type_group = QGroupBox("类型过滤")
        type_layout = QFormLayout()

        self._type_combo = QComboBox()
        self._type_combo.addItems(["全部", "文件夹", "文件"])
        type_layout.addRow("文件类型:", self._type_combo)

        self._extension_edit = QLineEdit()
        self._extension_edit.setPlaceholderText("例如: txt, pdf, jpg (用逗号分隔)")
        type_layout.addRow("扩展名:", self._extension_edit)

        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        option_group = QGroupBox("选项")
        option_layout = QVBoxLayout()

        self._show_hidden_check = QCheckBox("显示隐藏文件")
        self._show_hidden_check.setChecked(False)
        option_layout.addWidget(self._show_hidden_check)

        self._case_sensitive_check = QCheckBox("区分大小写")
        self._case_sensitive_check.setChecked(False)
        option_layout.addWidget(self._case_sensitive_check)

        option_group.setLayout(option_layout)
        layout.addWidget(option_group)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self._ok_button = QPushButton("应用")
        self._ok_button.setMinimumWidth(80)
        button_layout.addWidget(self._ok_button)

        self._cancel_button = QPushButton("取消")
        self._cancel_button.setMinimumWidth(80)
        button_layout.addWidget(self._cancel_button)

        layout.addLayout(button_layout)

    def _setup_connections(self):
        """建立信号槽连接"""
        self._ok_button.clicked.connect(self._on_apply)
        self._cancel_button.clicked.connect(self.reject)

    def _on_apply(self):
        """处理应用事件"""
        filter_config = {
            'name': self._name_edit.text().strip(),
            'type': self._type_combo.currentText(),
            'extension': self._extension_edit.text().strip(),
            'show_hidden': self._show_hidden_check.isChecked(),
            'case_sensitive': self._case_sensitive_check.isChecked()
        }
        self.filter_applied.emit(filter_config)
        self.accept()

    def get_filter_config(self) -> dict:
        """
        获取过滤配置

        Returns:
            过滤配置
        """
        return {
            'name': self._name_edit.text().strip(),
            'type': self._type_combo.currentText(),
            'extension': self._extension_edit.text().strip(),
            'show_hidden': self._show_hidden_check.isChecked(),
            'case_sensitive': self._case_sensitive_check.isChecked()
        }

    def set_filter_config(self, config: dict):
        """
        设置过滤配置

        Args:
            config: 过滤配置
        """
        self._name_edit.setText(config.get('name', ''))
        self._type_combo.setCurrentText(config.get('type', '全部'))
        self._extension_edit.setText(config.get('extension', ''))
        self._show_hidden_check.setChecked(config.get('show_hidden', False))
        self._case_sensitive_check.setChecked(config.get('case_sensitive', False))