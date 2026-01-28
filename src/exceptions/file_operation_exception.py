from .base_exception import BaseException


class FileOperationException(BaseException):
    """文件操作异常"""

    ERROR_CODE = 1001

    def __init__(self, message: str, error_code: int = ERROR_CODE):
        """
        初始化文件操作异常

        Args:
            message: 错误消息
            error_code: 错误码
        """
        super().__init__(message, error_code)


class FileNotFound(FileOperationException):
    """文件不存在异常"""

    ERROR_CODE = 1001

    def __init__(self, file_path: str):
        """
        初始化文件不存在异常

        Args:
            file_path: 文件路径
        """
        message = f"文件不存在: {file_path}"
        super().__init__(message, self.ERROR_CODE)


class FileExists(FileOperationException):
    """文件已存在异常"""

    ERROR_CODE = 1003

    def __init__(self, file_path: str):
        """
        初始化文件已存在异常

        Args:
            file_path: 文件路径
        """
        message = f"文件已存在: {file_path}"
        super().__init__(message, self.ERROR_CODE)


class FilePermissionDenied(FileOperationException):
    """文件权限不足异常"""

    ERROR_CODE = 1002

    def __init__(self, file_path: str):
        """
        初始化文件权限不足异常

        Args:
            file_path: 文件路径
        """
        message = f"文件权限不足: {file_path}"
        super().__init__(message, self.ERROR_CODE)