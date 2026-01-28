class BaseException(Exception):
    """基础异常类"""

    def __init__(self, message: str, error_code: int = 0):
        """
        初始化基础异常

        Args:
            message: 错误消息
            error_code: 错误码
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self) -> str:
        """返回错误消息"""
        return f"[{self.error_code}] {self.message}"