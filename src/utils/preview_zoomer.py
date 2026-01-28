from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF
from typing import Optional


class PreviewZoomer:
    """
    预览缩放工具
    提供预览内容的缩放功能
    """

    def __init__(self, widget: QWidget):
        """
        初始化缩放器

        Args:
            widget: 预览组件
        """
        self.widget = widget
        self._zoom_level = 1.0
        self._min_zoom = 0.1
        self._max_zoom = 10.0
        self._zoom_step = 0.1

    def zoom_in(self):
        """放大"""
        if self._zoom_level < self._max_zoom:
            self._zoom_level += self._zoom_step
            self._apply_zoom()

    def zoom_out(self):
        """缩小"""
        if self._zoom_level > self._min_zoom:
            self._zoom_level -= self._zoom_step
            self._apply_zoom()

    def reset_zoom(self):
        """重置缩放"""
        self._zoom_level = 1.0
        self._apply_zoom()

    def set_zoom_level(self, level: float):
        """
        设置缩放级别

        Args:
            level: 缩放级别
        """
        if self._min_zoom <= level <= self._max_zoom:
            self._zoom_level = level
            self._apply_zoom()

    def get_zoom_level(self) -> float:
        """
        获取缩放级别

        Returns:
            缩放级别
        """
        return self._zoom_level

    def set_zoom_step(self, step: float):
        """
        设置缩放步长

        Args:
            step: 缩放步长
        """
        if step > 0:
            self._zoom_step = step

    def get_zoom_step(self) -> float:
        """
        获取缩放步长

        Returns:
            缩放步长
        """
        return self._zoom_step

    def set_zoom_range(self, min_zoom: float, max_zoom: float):
        """
        设置缩放范围

        Args:
            min_zoom: 最小缩放
            max_zoom: 最大缩放
        """
        if min_zoom > 0 and max_zoom > min_zoom:
            self._min_zoom = min_zoom
            self._max_zoom = max_zoom

    def get_zoom_range(self) -> tuple:
        """
        获取缩放范围

        Returns:
            (最小缩放, 最大缩放)
        """
        return (self._min_zoom, self._max_zoom)

    def _apply_zoom(self):
        """应用缩放"""
        if hasattr(self.widget, 'setTransform'):
            from PySide6.QtGui import QTransform
            transform = QTransform().scale(self._zoom_level, self._zoom_level)
            self.widget.setTransform(transform)

    def can_zoom_in(self) -> bool:
        """
        判断是否可以放大

        Returns:
            是否可以放大
        """
        return self._zoom_level < self._max_zoom

    def can_zoom_out(self) -> bool:
        """
        判断是否可以缩小

        Returns:
            是否可以缩小
        """
        return self._zoom_level > self._min_zoom

    def get_zoom_percentage(self) -> int:
        """
        获取缩放百分比

        Returns:
            缩放百分比
        """
        return int(self._zoom_level * 100)