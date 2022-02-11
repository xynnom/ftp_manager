from pathlib import Path
from manager import ftp
from manager import credential
from manager import utils
import logging
import sys
import os




if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    target_dir = os.getcwd()
    ftp_credential = credential.FTPCredential(
        'test.rebex.net', 21, 'demo', 'password',
        True, False, Path(''), Path(''))

    with utils.transfer_manager(ftp.FTPConnector, ftp_credential) as f:
        file_handler = ftp.FTPFileHandler(f)
        print(file_handler.download_file(
              'readme.txt', f"{target_dir}\\readme.txt"))
