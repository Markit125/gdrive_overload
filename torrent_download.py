from qbittorrent import Client
import time
import os
import glob
import subprocess
from dotenv import load_dotenv
import loads_gdrive as lgd


load_dotenv()
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
    lgd.log_file("\nConnected\n\n")
    qb.login("Markit125", "MarkMark12")

    name = glob.glob('*.torrent')[0]
    start_download(name, qb)

    downd = False
    while True:
        # os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        torrents = qb.torrents()
        counter = len(torrents)
        for torrent in torrents:
            log = ''
            log += f"Torrent name: {torrent['name']}\n" \
            f"hash: {torrent['hash']}\n" \
            f"Seeds: {torrent['num_seeds']}\n" \
            f"File size: {get_size_format(torrent['total_size'])}\n" \
            f"Download speed: {get_size_format(torrent['dlspeed'])}/s\n" \
            f"Progress: {get_size_format(torrent['downloaded'])} / " \
            f"{get_size_format(torrent['total_size'])}"
            progress = round(torrent['downloaded'] / torrent['total_size'] * 100, 1)
            log += f"[{'|' * int(round(progress, 0) / 5)}" \
            f"{' ' * int(round(100 - progress, 0) / 5)}] {progress}%\n\n"
            lgd.log_file(log)
            if progress >= 100:
                counter -= 1
            if not counter:
                downd = True
        if downd:
            break
        time.sleep(15)

    lgd.log_file('Download completed\n')


def main():
    subprocess.call([QBITTORRENT_PATH])
    download_torrent()


if __name__ == '__main__':
    main()


