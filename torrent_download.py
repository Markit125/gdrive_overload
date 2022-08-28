from qbittorrent import Client
import time
import os
import glob
import subprocess
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
SAVEPATH = os.getenv('SAVEPATH')
QBITTORRENT_PATH = os.getenv('QBITTORRENT_PATH')

# https://www.thepythoncode.com/code/download-torrent-files-in-python

def start_download(filename, qb):
    torrent_file = open(filename, "rb")

    qb.download_from_file(torrent_file, savepath=SAVEPATH)

    # magnet_link = "magnet:?xt=urn:btih:e334ab9ddd91c10938a7....."
    # qb.download_from_link(magnet_link)

    # pause all downloads
    qb.pause_all()

    # resume them
    qb.resume_all()


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20 MB'
        1253656678 => '1.17 GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f} {unit}{suffix}"
        b /= factor
    return f"{b:.2f} Y{suffix}"


def download_torrent():
    qb = Client("http://127.0.0.1:8080/")
    print("\nConnected\n")
    qb.login(USERNAME, PASSWORD)

    name = glob.glob('*.torrent')[0]
    start_download(name, qb)

    downd = False
    while True:
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        torrents = qb.torrents()
        counter = len(torrents)
        for torrent in torrents:
            print(f"Torrent name: {torrent['name']}")
            print(f"hash: {torrent['hash']}")
            print(f"Seeds: {torrent['num_seeds']}")
            print(f"File size: {get_size_format(torrent['total_size'])}")
            print(f"Download speed: {get_size_format(torrent['dlspeed'])}/s")
            print(f"Progress: {get_size_format(torrent['downloaded'])} / ", end='')
            print(f"{get_size_format(torrent['total_size'])}")
            progress = round(torrent['downloaded'] / torrent['total_size'] * 100, 1)
            print(f"[{'|' * int(round(progress, 0) / 5)}", end='')
            print(f"{' ' * int(round(100 - progress, 0) / 5)}] {progress}%")
            print()
            if progress >= 100:
                counter -= 1
            if not counter:
                downd = True
        if downd:
            break
        time.sleep(15)

    print('Download complited')


def main():
    subprocess.call([QBITTORRENT_PATH])
    download_torrent()


if __name__ == '__main__':
    main()


