from .base_exception import BaseException


class FileSystemException(BaseException):
    """文件系统异常"""

    ERROR_CODE = 1008

    def __init__(self, message: str, error_code: int = ERROR_CODE):
        """
        初始化文件系统异常

        Args:
            message: 错误消息
            error_code: 错误码
        """
        super().__init__(message, error_code)


class NotADirectory(FileSystemException):
    """不是文件夹异常"""

    ERROR_CODE = 1004

    def __init__(self, path: str):
        """
        初始化不是文件夹异常

        Args:
            path: 路径
        """
        message = f"不是文件夹: {path}"
        super().__init__(message, self.ERROR_CODE)


class DirectoryNotEmpty(FileSystemException):
    """文件夹不为空异常"""

    ERROR_CODE = 1008

    def __init__(self, path: str):
        """
        初始化文件夹不为空异常

        Args:
            path: 路径
        """
        message = f"文件夹不为空: {path}"
        super().__init__(message, self.ERROR_CODE)


class InvalidPath(FileSystemException):
    """无效路径异常"""

    ERROR_CODE = 1008

    def __init__(self, path: str):
        """
        初始化无效路径异常

        Args:
            path: 路径
        """
        message = f"无效路径: {path}"
        super().__init__(message, self.ERROR_CODE)