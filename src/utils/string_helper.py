import re
from typing import List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


class StringHelper:
    """
    字符串辅助工具
    提供字符串处理功能
    """

    @staticmethod
    def is_empty(s: str) -> bool:
        """
        判断字符串是否为空

        Args:
            s: 字符串

        Returns:
            是否为空
        """
        return not s or s.strip() == ""

    @staticmethod
    def trim(s: str) -> str:
        """
        去除首尾空格

        Args:
            s: 字符串

        Returns:
            去除空格后的字符串
        """
        return s.strip()

    @staticmethod
    def to_lower(s: str) -> str:
        """
        转换为小写

        Args:
            s: 字符串

        Returns:
            小写字符串
        """
        return s.lower()

    @staticmethod
    def to_upper(s: str) -> str:
        """
        转换为大写

        Args:
            s: 字符串

        Returns:
            大写字符串
        """
        return s.upper()

    @staticmethod
    def capitalize(s: str) -> str:
        """
        首字母大写

        Args:
            s: 字符串

        Returns:
            首字母大写的字符串
        """
        return s.capitalize()

    @staticmethod
    def contains(s: str, substr: str, case_sensitive: bool = False) -> bool:
        """
        判断是否包含子串

        Args:
            s: 字符串
            substr: 子串
            case_sensitive: 是否区分大小写

        Returns:
            是否包含
        """
        if case_sensitive:
            return substr in s
        return substr.lower() in s.lower()

    @staticmethod
    def starts_with(s: str, prefix: str, case_sensitive: bool = False) -> bool:
        """
        判断是否以指定前缀开头

        Args:
            s: 字符串
            prefix: 前缀
            case_sensitive: 是否区分大小写

        Returns:
            是否以指定前缀开头
        """
        if case_sensitive:
            return s.startswith(prefix)
        return s.lower().startswith(prefix.lower())

    @staticmethod
    def ends_with(s: str, suffix: str, case_sensitive: bool = False) -> bool:
        """
        判断是否以指定后缀结尾

        Args:
            s: 字符串
            suffix: 后缀
            case_sensitive: 是否区分大小写

        Returns:
            是否以指定后缀结尾
        """
        if case_sensitive:
            return s.endswith(suffix)
        return s.lower().endswith(suffix.lower())

    @staticmethod
    def split(s: str, delimiter: str) -> List[str]:
        """
        分割字符串

        Args:
            s: 字符串
            delimiter: 分隔符

        Returns:
            分割后的字符串列表
        """
        return s.split(delimiter)

    @staticmethod
    def join(strings: List[str], delimiter: str = "") -> str:
        """
        连接字符串

        Args:
            strings: 字符串列表
            delimiter: 分隔符

        Returns:
            连接后的字符串
        """
        return delimiter.join(strings)

    @staticmethod
    def replace(s: str, old: str, new: str, count: int = -1) -> str:
        """
        替换字符串

        Args:
            s: 字符串
            old: 旧字符串
            new: 新字符串
            count: 替换次数（-1表示全部替换）

        Returns:
            替换后的字符串
        """
        return s.replace(old, new, count)

    @staticmethod
    def remove_whitespace(s: str) -> str:
        """
        去除所有空白字符

        Args:
            s: 字符串

        Returns:
            去除空白字符后的字符串
        """
        return re.sub(r'\s+', '', s)

    @staticmethod
    def truncate(s: str, max_length: int, suffix: str = "...") -> str:
        """
        截断字符串

        Args:
            s: 字符串
            max_length: 最大长度
            suffix: 后缀

        Returns:
            截断后的字符串
        """
        if len(s) <= max_length:
            return s
        return s[:max_length - len(suffix)] + suffix

    @staticmethod
    def pad_left(s: str, length: int, char: str = " ") -> str:
        """
        左侧填充

        Args:
            s: 字符串
            length: 目标长度
            char: 填充字符

        Returns:
            填充后的字符串
        """
        return s.rjust(length, char)

    @staticmethod
    def pad_right(s: str, length: int, char: str = " ") -> str:
        """
        右侧填充

        Args:
            s: 字符串
            length: 目标长度
            char: 填充字符

        Returns:
            填充后的字符串
        """
        return s.ljust(length, char)

    @staticmethod
    def is_numeric(s: str) -> bool:
        """
        判断是否为数字

        Args:
            s: 字符串

        Returns:
            是否为数字
        """
        try:
            float(s)
            return True
        except Exception:
            return False

    @staticmethod
    def is_alpha(s: str) -> bool:
        """
        判断是否为字母

        Args:
            s: 字符串

        Returns:
            是否为字母
        """
        return s.isalpha()

    @staticmethod
    def is_alphanumeric(s: str) -> bool:
        """
        判断是否为字母数字

        Args:
            s: 字符串

        Returns:
            是否为字母数字
        """
        return s.isalnum()

    @staticmethod
    def count_occurrences(s: str, substr: str) -> int:
        """
        统计子串出现次数

        Args:
            s: 字符串
            substr: 子串

        Returns:
            出现次数
        """
        return s.count(substr)

    @staticmethod
    def reverse(s: str) -> str:
        """
        反转字符串

        Args:
            s: 字符串

        Returns:
            反转后的字符串
        """
        return s[::-1]

    @staticmethod
    def to_snake_case(s: str) -> str:
        """
        转换为蛇形命名

        Args:
            s: 字符串

        Returns:
            蛇形命名字符串
        """
        s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
        s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)
        return s.lower()

    @staticmethod
    def to_camel_case(s: str) -> str:
        """
        转换为驼峰命名

        Args:
            s: 字符串

        Returns:
            驼峰命名字符串
        """
        components = s.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def to_pascal_case(s: str) -> str:
        """
        转换为帕斯卡命名

        Args:
            s: 字符串

        Returns:
            帕斯卡命名字符串
        """
        components = s.split('_')
        return ''.join(x.title() for x in components)

    @staticmethod
    def escape_html(s: str) -> str:
        """
        转义HTML特殊字符

        Args:
            s: 字符串

        Returns:
            转义后的字符串
        """
        html_escape = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;'
        }
        return ''.join(html_escape.get(c, c) for c in s)

    @staticmethod
    def unescape_html(s: str) -> str:
        """
        反转义HTML特殊字符

        Args:
            s: 字符串

        Returns:
            反转义后的字符串
        """
        html_unescape = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#x27;': "'"
        }
        for key, value in html_unescape.items():
            s = s.replace(key, value)
        return s

    @staticmethod
    def format_bytes(size: int) -> str:
        """
        格式化字节数

        Args:
            size: 字节数

        Returns:
            格式化后的字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    @staticmethod
    def mask(s: str, visible_chars: int = 4, mask_char: str = "*") -> str:
        """
        掩码字符串

        Args:
            s: 字符串
            visible_chars: 可见字符数
            mask_char: 掩码字符

        Returns:
            掩码后的字符串
        """
        if len(s) <= visible_chars:
            return s
        return s[:visible_chars] + mask_char * (len(s) - visible_chars)

    @staticmethod
    def generate_random(length: int = 8) -> str:
        """
        生成随机字符串

        Args:
            length: 长度

        Returns:
            随机字符串
        """
        import random
        import string
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))