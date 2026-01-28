from datetime import datetime
from typing import Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


class DateTimeHelper:
    """
    日期时间辅助工具
    提供日期时间处理功能
    """

    DATE_FORMATS = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y"
    ]

    @staticmethod
    def now() -> datetime:
        """
        获取当前时间

        Returns:
            当前时间
        """
        return datetime.now()

    @staticmethod
    def from_timestamp(timestamp: float) -> datetime:
        """
        从时间戳创建时间

        Args:
            timestamp: 时间戳

        Returns:
            时间对象
        """
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def to_timestamp(dt: datetime) -> float:
        """
        转换为时间戳

        Args:
            dt: 时间对象

        Returns:
            时间戳
        """
        return dt.timestamp()

    @staticmethod
    def format(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        格式化时间

        Args:
            dt: 时间对象
            format_str: 格式字符串

        Returns:
            格式化后的时间字符串
        """
        return dt.strftime(format_str)

    @staticmethod
    def parse(date_str: str) -> Optional[datetime]:
        """
        解析时间字符串

        Args:
            date_str: 时间字符串

        Returns:
            时间对象
        """
        for fmt in DateTimeHelper.DATE_FORMATS:
            try:
                return datetime.strptime(date_str, fmt)
            except Exception:
                continue
        return None

    @staticmethod
    def format_file_time(timestamp: float) -> str:
        """
        格式化文件时间

        Args:
            timestamp: 时间戳

        Returns:
            格式化后的时间字符串
        """
        dt = DateTimeHelper.from_timestamp(timestamp)
        now = DateTimeHelper.now()
        delta = now - dt

        if delta.days == 0:
            if delta.seconds < 60:
                return "刚刚"
            elif delta.seconds < 3600:
                minutes = delta.seconds // 60
                return f"{minutes}分钟前"
            else:
                hours = delta.seconds // 3600
                return f"{hours}小时前"
        elif delta.days == 1:
            return "昨天"
        elif delta.days < 7:
            return f"{delta.days}天前"
        else:
            return DateTimeHelper.format(dt, "%Y-%m-%d")

    @staticmethod
    def format_size(size: int) -> str:
        """
        格式化大小

        Args:
            size: 大小（字节）

        Returns:
            格式化后的大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    @staticmethod
    def get_age(dt: datetime) -> str:
        """
        获取时间年龄

        Args:
            dt: 时间对象

        Returns:
            年龄字符串
        """
        return DateTimeHelper.format_file_time(DateTimeHelper.to_timestamp(dt))

    @staticmethod
    def is_today(dt: datetime) -> bool:
        """
        判断是否为今天

        Args:
            dt: 时间对象

        Returns:
            是否为今天
        """
        today = DateTimeHelper.now()
        return dt.date() == today.date()

    @staticmethod
    def is_yesterday(dt: datetime) -> bool:
        """
        判断是否为昨天

        Args:
            dt: 时间对象

        Returns:
            是否为昨天
        """
        yesterday = DateTimeHelper.now()
        yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_dt = yesterday.replace(day=yesterday.day - 1)
        return dt.date() == yesterday_dt.date()

    @staticmethod
    def diff(dt1: datetime, dt2: datetime) -> str:
        """
        计算时间差

        Args:
            dt1: 时间对象1
            dt2: 时间对象2

        Returns:
            时间差字符串
        """
        delta = dt2 - dt1
        total_seconds = delta.total_seconds()

        if total_seconds < 60:
            return f"{int(total_seconds)}秒"
        elif total_seconds < 3600:
            minutes = int(total_seconds / 60)
            return f"{minutes}分钟"
        elif total_seconds < 86400:
            hours = int(total_seconds / 3600)
            return f"{hours}小时"
        else:
            days = int(total_seconds / 86400)
            return f"{days}天"

    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """
        增加天数

        Args:
            dt: 时间对象
            days: 天数

        Returns:
            新的时间对象
        """
        from datetime import timedelta
        return dt + timedelta(days=days)

    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """
        增加小时数

        Args:
            dt: 时间对象
            hours: 小时数

        Returns:
            新的时间对象
        """
        from datetime import timedelta
        return dt + timedelta(hours=hours)

    @staticmethod
    def add_minutes(dt: datetime, minutes: int) -> datetime:
        """
        增加分钟数

        Args:
            dt: 时间对象
            minutes: 分钟数

        Returns:
            新的时间对象
        """
        from datetime import timedelta
        return dt + timedelta(minutes=minutes)