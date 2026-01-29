from PySide6.QtWidgets import QStatusBar, QLabel, QWidget, QHBoxLayout, QProgressBar
from PySide6.QtCore import QObject, Signal, Qt


class StatusBarSignals(QObject):
    """状态栏信号"""

    path_changed = Signal(str)
    file_count_changed = Signal(int)
    selection_changed = Signal(str)
    operation_changed = Signal(str)


class StatusBar(QStatusBar):
    """状态栏组件"""

    def __init__(self, parent=None):
        """
        初始化状态栏

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.signals = StatusBarSignals()
        self._setup_ui()

    def _setup_ui(self):
        """设置界面"""
        self._setup_path_label()
        self._setup_file_count_label()
        self._setup_selection_label()
        self._setup_operation_label()
        self._setup_progress_bar()

    def _setup_path_label(self):
        """设置路径标签"""
        self._path_label = QLabel("当前路径: 未选择")
        self._path_label.setMinimumWidth(200)
        self.addWidget(self._path_label, 1)

    def _setup_file_count_label(self):
        """设置文件数量标签"""
        self._file_count_label = QLabel("文件数: 0")
        self._file_count_label.setMinimumWidth(100)
        self.addPermanentWidget(self._file_count_label)

    def _setup_selection_label(self):
        """设置选中信息标签"""
        self._selection_label = QLabel("选中: 无")
        self._selection_label.setMinimumWidth(150)
        self.addPermanentWidget(self._selection_label)

    def _setup_operation_label(self):
        """设置操作状态标签"""
        self._operation_label = QLabel("就绪")
        self._operation_label.setMinimumWidth(100)
        self.addPermanentWidget(self._operation_label)

    def _setup_progress_bar(self):
        """设置进度条"""
        self._progress_bar = QProgressBar()
        self._progress_bar.setMaximumWidth(200)
        self._progress_bar.setVisible(False)
        self.addPermanentWidget(self._progress_bar)

    def set_path(self, path: str):
        """
        设置当前路径

        Args:
            path: 路径
        """
        if path:
            self._path_label.setText(f"当前路径: {path}")
            self.signals.path_changed.emit(path)
        else:
            self._path_label.setText("当前路径: 未选择")

    def get_path(self) -> str:
        """
        获取当前路径

        Returns:
            当前路径
        """
        text = self._path_label.text()
        if text.startswith("当前路径: "):
            return text[6:]
        return ""

    def set_file_count(self, count: int):
        """
        设置文件数量

        Args:
            count: 文件数量
        """
        self._file_count_label.setText(f"文件数: {count}")
        self.signals.file_count_changed.emit(count)

    def set_selection(self, selection: str):
        """
        设置选中信息

        Args:
            selection: 选中信息
        """
        if selection:
            self._selection_label.setText(f"选中: {selection}")
            self.signals.selection_changed.emit(selection)
        else:
            self._selection_label.setText("选中: 无")

    def get_selection(self) -> str:
        """
        获取选中信息

        Returns:
            选中信息
        """
        text = self._selection_label.text()
        if text.startswith("选中: ") and text != "选中: 无":
            return text[4:]
        return ""

    def set_operation(self, operation: str):
        """
        设置操作状态

        Args:
            operation: 操作状态
        """
        if operation:
            self._operation_label.setText(operation)
            self.signals.operation_changed.emit(operation)
        else:
            self._operation_label.setText("就绪")

    def show_progress(self, value: int, maximum: int = 100):
        """
        显示进度

        Args:
            value: 当前进度
            maximum: 最大进度
        """
        self._progress_bar.setMaximum(maximum)
        self._progress_bar.setValue(value)
        self._progress_bar.setVisible(True)

    def hide_progress(self):
        """隐藏进度条"""
        self._progress_bar.setVisible(False)

    def update_progress(self, value: int):
        """
        更新进度

        Args:
            value: 当前进度
        """
        self._progress_bar.setValue(value)

    def clear(self):
        """清除状态栏信息"""
        self._path_label.setText("当前路径: 未选择")
        self._file_count_label.setText("文件数: 0")
        self._selection_label.setText("选中: 无")
        self._operation_label.setText("就绪")
        self.hide_progress()