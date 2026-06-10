class AppError(Exception):
    """应用基础异常"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    """资源不存在"""

    def __init__(self, resource: str = "资源"):
        super().__init__(f"{resource}不存在", 404)


class ValidationError(AppError):
    """参数校验失败"""

    def __init__(self, message: str):
        super().__init__(message, 400)
