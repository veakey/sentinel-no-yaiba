"""
Custom exceptions for the application
"""


class AppException(Exception):
    """Base exception for the application"""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ProviderException(AppException):
    """Exception related to provider operations"""
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


class CacheException(AppException):
    """Exception related to cache operations"""
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)

