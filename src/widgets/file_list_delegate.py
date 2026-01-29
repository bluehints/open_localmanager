from PySide6.QtWidgets import QStyledItemDelegate, QApplication, QStyle
from PySide6.QtCore import QSize, Qt, QRect, QEvent
from PySide6.QtGui import QPainter, QIcon, QFont, QColor
from typing import Optional
from models.file_item import FileItem


class FileListDelegate(QStyledItemDelegate):
    """文件列表代理"""

    def __init__(self, parent=None):
        """
        初始化文件列表代理

        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self._icon_size = QSize(24, 24)
        self._text_margin = 8
        self._icon_spacing = 8

    def paint(self, painter: QPainter, option, index):
        """
        绘制项目

        Args:
            painter: 绘制器
            option: 绘制选项
            index: 模型索引
        """
        painter.save()

        background_rect = option.rect
        if option.state & QStyle.State_Selected:
            painter.fillRect(background_rect, option.palette.highlight())
        else:
            painter.fillRect(background_rect, option.palette.base())

        icon_rect = self._get_icon_rect(option)
        text_rect = self._get_text_rect(option, icon_rect)

        self._paint_icon(painter, option, index, icon_rect)
        self._paint_text(painter, option, index, text_rect)

        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        """
        获取项目大小提示

        Args:
            option: 绘制选项
            index: 模型索引

        Returns:
            项目大小
        """
        height = max(self._icon_size.height(), option.fontMetrics.height())
        height += self._text_margin * 2
        return QSize(option.rect.width(), height)

    def _get_icon_rect(self, option) -> QRect:
        """
        获取图标矩形

        Args:
            option: 绘制选项

        Returns:
            图标矩形
        """
        x = option.rect.left() + self._text_margin
        y = option.rect.top() + (option.rect.height() - self._icon_size.height()) // 2
        return QRect(x, y, self._icon_size.width(), self._icon_size.height())

    def _get_text_rect(self, option, icon_rect: QRect) -> QRect:
        """
        获取文本矩形

        Args:
            option: 绘制选项
            icon_rect: 图标矩形

        Returns:
            文本矩形
        """
        x = icon_rect.right() + self._icon_spacing
        y = option.rect.top() + self._text_margin
        width = option.rect.width() - x - option.rect.left() - self._text_margin
        height = option.rect.height() - self._text_margin * 2
        return QRect(x, y, width, height)

    def _paint_icon(self, painter: QPainter, option, index, icon_rect: QRect):
        """
        绘制图标

        Args:
            painter: 绘制器
            option: 绘制选项
            index: 模型索引
            icon_rect: 图标矩形
        """
        source_model = index.model()
        if hasattr(source_model, 'sourceModel'):
            source_model = source_model.sourceModel()

        file_item = source_model.get_file(index) if hasattr(source_model, 'get_file') else None

        if file_item:
            icon = self._get_file_icon(file_item)
            if icon:
                icon.paint(painter, icon_rect)

    def _paint_text(self, painter: QPainter, option, index, text_rect: QRect):
        """
        绘制文本

        Args:
            painter: 绘制器
            option: 绘制选项
            index: 模型索引
            text_rect: 文本矩形
        """
        source_model = index.model()
        if hasattr(source_model, 'sourceModel'):
            source_model = source_model.sourceModel()

        file_item = source_model.get_file(index) if hasattr(source_model, 'get_file') else None

        if file_item:
            text = file_item.name
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, text)

    def _get_file_icon(self, file_item: FileItem) -> Optional[QIcon]:
        """
        获取文件图标

        Args:
            file_item: 文件项

        Returns:
            文件图标
        """
        from utils.icon_provider import IconProvider
        icon_provider = IconProvider()

        if file_item.is_folder:
            return icon_provider.get_folder_icon()
        else:
            return icon_provider.get_file_icon(file_item.path)

    def editorEvent(self, event, model, option, index) -> bool:
        """
        编辑器事件

        Args:
            event: 事件
            model: 模型
            option: 选项
            index: 索引

        Returns:
            是否处理事件
        """
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                return True
        return False
