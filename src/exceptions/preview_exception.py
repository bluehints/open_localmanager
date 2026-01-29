from .base_exception import BaseException


class PreviewException(BaseException):
    """预览异常"""

    ERROR_CODE = 1007

    def __init__(self, message: str, error_code: int = ERROR_CODE):
        """
        初始化预览异常

        Args:
            message: 错误消息
            error_code: 错误码
        """
        super().__init__(message, error_code)


class UnsupportedFileType(PreviewException):
    """不支持的文件类型异常"""

    ERROR_CODE = 1007

    def __init__(self, file_path: str):
        """
        初始化不支持的文件类型异常

        Args:
            file_path: 文件路径
        """
        message = f"不支持的文件类型: {file_path}"
        super().__init__(message, self.ERROR_CODE)


class PreviewFailed(PreviewException):
    """预览失败异常"""

    ERROR_CODE = 1007

    def __init__(self, file_path: str, reason: str):
        """
        初始化预览失败异常

        Args:
            file_path: 文件路径
            reason: 失败原因
        """
        message = f"预览失败: {file_path}, 原因: {reason}"
        super().__init__(message, self.ERROR_CODE)