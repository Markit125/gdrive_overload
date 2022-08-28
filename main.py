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
    files = os.listdir('Downloads/')
    for file in files:
        if '.torrent' in file:
            os.remove(f'Downloads/{file}')

    files = set(os.listdir('Downloads/'))

    if not lgd.download_file(folder=GDRIVE_FOLDER, torrent=True):
        print('No file')
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
    os.remove(glob.glob('*.torrent')[0])
    lgd.upload_file(file_path=f'Downloads/{new_dir}.tgz', folder=GDRIVE_FOLDER)
    subprocess.call("TASKKILL /F /IM qbittorrent.exe", shell=True)

if __name__ == '__main__':
    main()
