from dataclasses import dataclass, field
import pathlib


@dataclass
class Credential:
    host: str
    port: int
    username: str = field(repr=False, default='')
    password: str = field(repr=False, default='')

    @property
    def source(self):
        return f'{self.host}:{self.port}'

    # This function should be on the Credential Registration class
    # def __post_init__(self):
    #     # Do encryption here


@dataclass
class FTPCredential(Credential):
    port: int = 21
    active: bool = field(default=False)
    ftps: bool = False
    cert_file: pathlib.Path = field(default=pathlib.Path(""))
    key_file: pathlib.Path = field(default=pathlib.Path(""))

    def __repr__(self):
        return f'host: {self.source} | username:{self.username}'

    @property
    def protocol(self):
        return 'ftp'


def check_creds(cred: Credential) -> str:
    return cred.__repr__()
