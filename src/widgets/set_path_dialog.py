from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QMessageBox
)
from PySide6.QtCore import Qt, Signal
from pathlib import Path
import os


class SetPathDialog(QDialog):
    """设置路径对话框"""

    path_selected = Signal(str)

    def __init__(self, current_path: str = "", parent=None):
        """
        初始化对话框

        Args:
            current_path: 当前路径
            parent: 父窗口
        """
        super().__init__(parent)
        self.current_path = current_path
        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("设置管理路径")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        layout = QVBoxLayout(self)

        path_label = QLabel("管理路径:")
        layout.addWidget(path_label)

        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setText(self.current_path)
        path_layout.addWidget(self.path_edit)

        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self._on_browse_clicked)
        path_layout.addWidget(browse_button)

        layout.addLayout(path_layout)

        recent_label = QLabel("最近使用的路径:")
        layout.addWidget(recent_label)

        self.recent_list = QListWidget()
        self._load_recent_paths()
        layout.addWidget(self.recent_list)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self._on_ok_clicked)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def _load_recent_paths(self):
        """加载最近使用的路径"""
        self.recent_list.clear()

        home_dir = Path.home()
        common_paths = [
            str(home_dir),
            str(home_dir / "Documents"),
            str(home_dir / "Desktop"),
            str(home_dir / "Downloads"),
            "C:\\",
            "D:\\",
            "E:\\"
        ]

        for path in common_paths:
            if os.path.exists(path):
                item = QListWidgetItem(path)
                self.recent_list.addItem(item)

    def _on_browse_clicked(self):
        """浏览按钮点击事件"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if dialog.exec():
            selected_files = dialog.selectedFiles()
            if selected_files:
                self.path_edit.setText(selected_files[0])

    def _on_ok_clicked(self):
        """确定按钮点击事件"""
        path = self.path_edit.text().strip()

        if not path:
            QMessageBox.warning(self, "警告", "请输入路径")
            return

        if not os.path.exists(path):
            QMessageBox.warning(self, "警告", "路径不存在")
            return

        if not os.path.isdir(path):
            QMessageBox.warning(self, "警告", "请选择文件夹")
            return

        self.path_selected.emit(path)
        self.accept()

    def get_selected_path(self) -> str:
        """
        获取选中的路径

        Returns:
            选中路径
        """
        return self.path_edit.text().strip()