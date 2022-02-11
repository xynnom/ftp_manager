from abc import ABC, abstractmethod
import pathlib


class Connector(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def quit(self) -> None:
        pass

    @abstractmethod
    def check_status(self, interval):
        pass


class FileHandler(ABC):
    @abstractmethod
    def file_exists(self, filename) -> bool:
        pass

    @abstractmethod
    def download_file(self, filename: str, target_dir: pathlib.Path) -> str:
        pass

    @abstractmethod
    def upload_file(self, filename: pathlib.Path, target_dir: str) -> str:
        pass

    @abstractmethod
    def rename_temp_file(self, temp_file_name, final_name) -> None:
        pass
    
    
