from .base_exception import BaseException


class ConfigException(BaseException):
    """配置异常"""

    ERROR_CODE = 1005

    def __init__(self, message: str, error_code: int = ERROR_CODE):
        """
        初始化配置异常

        Args:
            message: 错误消息
            error_code: 错误码
        """
        super().__init__(message, error_code)


class ConfigKeyNotFound(ConfigException):
    """配置键不存在异常"""

    ERROR_CODE = 1005

    def __init__(self, key: str):
        """
        初始化配置键不存在异常

        Args:
            key: 配置键
        """
        message = f"配置键不存在: {key}"
        super().__init__(message, self.ERROR_CODE)


class ConfigValueInvalid(ConfigException):
    """配置值无效异常"""

    ERROR_CODE = 1006

    def __init__(self, key: str, value: str):
        """
        初始化配置值无效异常

        Args:
            key: 配置键
            value: 配置值
        """
        message = f"配置值无效: {key} = {value}"
        super().__init__(message, self.ERROR_CODE)


class ConfigFileNotFound(ConfigException):
    """配置文件不存在异常"""

    ERROR_CODE = 1009

    def __init__(self, file_path: str):
        """
        初始化配置文件不存在异常

        Args:
            file_path: 配置文件路径
        """
        message = f"配置文件不存在: {file_path}"
        super().__init__(message, self.ERROR_CODE)