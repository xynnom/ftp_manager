"""FTP errors"""


class FTPError(Exception):
    """Errors for FTP connectors"""


class NotConnectedError(FTPError):
    """Raised when there is no connection established."""


class AuthenticationFailure(FTPError):
    """Passed wrong credentials"""


class CannotConnectviaSSL(FTPError):
    """No OpenSSL library installed"""


class FileDoesNotExist(FTPError):
    """File Does Not Exist"""
