import os
from typing import Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSlider
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from .base_previewer import BasePreviewer


class AudioPreviewer(BasePreviewer):
    """音频预览器"""

    AUDIO_EXTENSIONS = {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
        '.aiff', '.au', '.ra', '.mid', '.midi', '.ac3', '.dts',
        '.amr', '.3gp', '.gsm', '.caf', '.tta', '.ape', '.wv'
    }

    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化音频预览器

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        self.widget = QWidget(self.parent)
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(10, 10, 10, 10)

        info_layout = QHBoxLayout()
        self.title_label = QLabel("音频预览", self.widget)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        info_layout.addWidget(self.title_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)

        self.cover_label = QLabel(self.widget)
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover_label.setMinimumHeight(200)
        self.cover_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        self.cover_label.setText("🎵")
        self.cover_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0; font-size: 80px;")
        layout.addWidget(self.cover_label)

        self.file_name_label = QLabel("未选择文件", self.widget)
        self.file_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_name_label.setStyleSheet("color: #666;")
        layout.addWidget(self.file_name_label)

        control_layout = QHBoxLayout()

        self.play_button = QPushButton("播放", self.widget)
        self.play_button.setMinimumWidth(80)
        self.play_button.clicked.connect(self._toggle_playback)
        control_layout.addWidget(self.play_button)

        self.stop_button = QPushButton("停止", self.widget)
        self.stop_button.setMinimumWidth(80)
        self.stop_button.clicked.connect(self._stop_playback)
        control_layout.addWidget(self.stop_button)

        layout.addLayout(control_layout)

        self.position_slider = QSlider(Qt.Orientation.Horizontal, self.widget)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self._set_position)
        self.position_slider.sliderPressed.connect(self._slider_pressed)
        self.position_slider.sliderReleased.connect(self._slider_released)
        layout.addWidget(self.position_slider)

        time_layout = QHBoxLayout()
        self.time_label = QLabel("00:00 / 00:00", self.widget)
        time_layout.addWidget(self.time_label)
        time_layout.addStretch()

        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("音量:", self.widget))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self.widget)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.valueChanged.connect(self._set_volume)
        volume_layout.addWidget(self.volume_slider)
        time_layout.addLayout(volume_layout)

        layout.addLayout(time_layout)

        self.media_player.positionChanged.connect(self._position_changed)
        self.media_player.durationChanged.connect(self._duration_changed)
        self.media_player.playbackStateChanged.connect(self._state_changed)

        self._slider_pressed = False

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
        return ext.lower() in self.AUDIO_EXTENSIONS

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

            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.file_name_label.setText(os.path.basename(file_path))
            self.media_player.play()
            self.current_path = file_path
            return True
        except Exception:
            return False

    def clear(self) -> None:
        """清空预览"""
        self._stop_playback()
        self.media_player.setSource(QUrl())
        self.current_path = None
        self.file_name_label.setText("未选择文件")
        self.time_label.setText("00:00 / 00:00")
        self.position_slider.setValue(0)

    def get_widget(self) -> QWidget:
        """
        获取预览窗口部件

        Returns:
            预览窗口部件
        """
        return self.widget

    def _toggle_playback(self):
        """切换播放/暂停"""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def _stop_playback(self):
        """停止播放"""
        self.media_player.stop()

    def _set_position(self, position: int):
        """
        设置播放位置

        Args:
            position: 位置（毫秒）
        """
        if self._slider_pressed:
            self.media_player.setPosition(position)

    def _slider_pressed(self):
        """滑块按下"""
        self._slider_pressed = True

    def _slider_released(self):
        """滑块释放"""
        self._slider_pressed = False

    def _set_volume(self, volume: int):
        """
        设置音量

        Args:
            volume: 音量值（0-100）
        """
        self.audio_output.setVolume(volume / 100.0)

    def _position_changed(self, position: int):
        """
        播放位置改变

        Args:
            position: 新位置（毫秒）
        """
        if not self._slider_pressed:
            self.position_slider.setValue(position)

        current_time = self._format_time(position)
        duration = self.media_player.duration()
        total_time = self._format_time(duration)
        self.time_label.setText(f"{current_time} / {total_time}")

    def _duration_changed(self, duration: int):
        """
        音频时长改变

        Args:
            duration: 时长（毫秒）
        """
        self.position_slider.setRange(0, duration)

    def _state_changed(self, state: QMediaPlayer.PlaybackState):
        """
        播放状态改变

        Args:
            state: 新状态
        """
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setText("暂停")
        else:
            self.play_button.setText("播放")

    def _format_time(self, milliseconds: int) -> str:
        """
        格式化时间

        Args:
            milliseconds: 毫秒数

        Returns:
            格式化的时间字符串
        """
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"