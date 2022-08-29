from torrent_download import QBITTORRENT_PATH, download_torrent
import loads_gdrive as lgd
import os
import tarfile
import subprocess
import glob
from dotenv import load_dotenv

load_dotenv()
QBITTORRENT_PATH = os.getenv('QBITTORRENT_PATH')

# folder from gdrive url like '1c4id6My-LmSOZDvTfEHOsf6SpXZSvw0E'
GDRIVE_FOLDER = os.getenv('GDRIVE_FOLDER')

def main():
    try:
        files = os.listdir('.')
        for file in files:
            if '.torrent' in file:
                os.remove(f'{file}')

        files = set(os.listdir('Downloads/'))

        if not lgd.download_file(folder=GDRIVE_FOLDER, torrent=True):
            lgd.log_file('No file')
            return

        # path to exec qbittorrent file
        subprocess.call([QBITTORRENT_PATH])
        download_torrent()
        
        new_dir = None
        for directory in set(os.listdir('Downloads/')) - files:
            new_dir = directory
        if new_dir is None:
            return
        
        with tarfile.open(f'Downloads/{new_dir}.tgz', 'w:gz') as tar:
            tar.add(f'Downloads/{new_dir}')
        
        lgd.upload_file(file_path=f'Downloads/{new_dir}.tgz', folder=GDRIVE_FOLDER)
        os.remove(f'Downloads/{new_dir}')
        
                
    except Exception as ex:
        lgd.log_file(f'\n{ex}')
    finally:
        os.remove(glob.glob('*.torrent')[0])
        subprocess.call("autoremove-torrents -c config.yaml", shell=True)
        subprocess.call("TASKKILL /F /IM qbittorrent.exe", shell=True)
        for file in os.listdir('.'):
            if 'log' in file:
                os.remove(f'{file}')

if __name__ == '__main__':
    main()
