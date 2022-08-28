from torrent_download import download_torrent
import loads_gdrive as lgd
import os
import tarfile
import subprocess
import glob


def main():
    files = os.listdir('Downloads/')
    for file in files:
        if '.torrent' in file:
            os.remove(f'Downloads/{file}')

    files = set(os.listdir('Downloads/'))

    # folder from gdrive url
    folder = '1c4id6My-LmSOZDvTfEHOsf6VpXZSvw0E'

    if not lgd.download_file(folder=folder, torrent=True):
        print('No file')
        return

    # path to exec qbittorrent file
    subprocess.call(['../qBittorrent/qbittorrent.exe'])
    download_torrent()
    
    new_dir = None
    for directory in set(os.listdir('Downloads/')) - files:
        new_dir = directory
    if new_dir is None:
        return
    
    with tarfile.open(f'Downloads/{new_dir}.tgz', 'w:gz') as tar:
        tar.add(f'Downloads/{new_dir}')
    os.remove(glob.glob('*.torrent')[0])
    lgd.upload_file(file_path=f'Downloads/{new_dir}.tgz', folder=folder)
    subprocess.call("TASKKILL /F /IM qbittorrent.exe", shell=True)

if __name__ == '__main__':
    main()
