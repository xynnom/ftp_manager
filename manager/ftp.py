from .base import Connector, FileHandler
from .errors import CannotConnectviaSSL
from .utils import retry
from ftplib import FTP
import ftplib
import logging
import pathlib
import ssl


log = logging.getLogger(__name__)


class FTPConnector(Connector):

    def __init__(self, credential) -> None:
        self.__credential = credential
        self._connector = FTP()

    @property
    def connector(self):
        return self._connector

    def connect(self):  # -> FTP
        log.info("Opening connection.")
        ftp = self.get_connection()
        # Need try except
        if self.__credential.password:
            log.info(f'{self.__credential.username}-{self.__credential.password}')   
            ftp.login(self.__credential.username, self.__credential.password)
        else:
            ftp.login(self.__credential.username)
        if self.__credential.ftps:
            ftp.prot_p()
        self._connector = ftp
        return ftp

    def get_connection(self):  # -> FTP:
        if self.__credential.active:
            return self.connect_active()
        if self.__credential.ftps:
            return self.connect_ftps()
        return self.connect_passive()

    def check_status(self, interval): # -> None:
        return super().check_status(interval)

    def quit(self) -> None:
        log.info("Connection closing.")
        try:
            self._connector.quit()
        except Exception:
            self._connector.close()

    def set_up_tls_context(self, cert_file: pathlib.Path,
                           key_file: pathlib.Path) -> ssl.SSLContext:
        """Setting up the SSL Context
        Args:
            cert_file (filepath, optional): Certificate file for TLS/SSL
                connecton. Defaults to None.
            key_file (filepath, optional): Key File for TLS/SSL
                connecton. Defaults to None.
        Raises:
            CannotConnectviaSSL: Certificate and Key File is missing
        Returns:
            ssl.SSLContext: Used for TLS/SSL connection
        """
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.load_cert_chain(cert_file, key_file)
            return context
        except Exception:
            raise CannotConnectviaSSL
        

    def connect_ftps(self):
        context = self.set_up_tls_context(
            cert_file=self._cert_file, key_file=self._key_file)
        ftp = CustomFTP_TLS(self.__credential.host, context=context)
        return ftp

    def connect_active(self):
        ftp = FTP()
        ftp.set_pasv(False)
        ftp.connect(self.__credential.host, self.__credential.port)
        return ftp

    def connect_passive(self):
        ftp = FTP(self.__credential.host)
        return ftp


class FTPFileHandler(FileHandler):

    def __init__(self, ftp_connector: FTP, max_retries: int = 3):
        self._connector = ftp_connector
        self.max_retries = max_retries

    def file_exists(self, filename: str) -> bool:
        try:
            return len(self._connector.nlst(filename)) > 0
        except Exception:
            raise FileNotFoundError

    def upload_file(self, filename: pathlib.Path, target_dir:  str) -> str:
        if not filename.is_file():
            log.error(f"File Not Found {filename}.")
            raise FileNotFoundError(filename)
        with open(filename, 'rb') as fp:
            self._connector.storbinary(f'STOR {target_dir}', fp)
        log.info(f"{filename} has been uploaded")
        return target_dir

    @retry(FileNotFoundError, logger=log)
    def download_file(self, filename: str, target_dir: pathlib.Path) -> str:
        if self.file_exists(filename):
            with open(f"{target_dir}", 'wb') as df:
                self._connector.retrbinary(f'RETR {filename}', df.write)
        return filename

    def rename_temp_file(self, temp_file_name: str, final_name: str) -> None:
        return super().rename_temp_file(temp_file_name, final_name)

    def nlst(self, directory=''):
        """Re-implement nlst of FTP
        """
        
        return self._connector.nlst(directory)

    

class CustomFTP_TLS(ftplib.FTP_TLS):
    """Explicit FTPS, with shared TLS session"""
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            session = self.sock.session
            if isinstance(self.sock, ssl.SSLSocket):
                session = self.sock.session
            conn = self.context.wrap_socket(
                    conn, server_hostname=self.host, session=session)
        return conn, size

