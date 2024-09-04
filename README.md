# gdrive_overload
An automation tool for downloading a torrent file (e.g., a Linux distribution) to a remote computer and uploading it to Google Drive, with logging and the ability to track progress via the console.

Needed client_secret.json is file from console.cloud.google.com

Algoritm
1. Check gdrive for torrent file
2. Download torrent file
3. Download files via qBittorrent
4. Upload them to gdrive


USERNAME and PASSWORD of qBittorrent should be replaced in torrent_download.py and config.yaml files!

Example of .env:

SAVEPATH = 'D:/МАРК/Torrent_overload/Downloads' \
QBITTORRENT_PATH = '../qBittorrent/qbittorrent.exe' \
GDRIVE_FOLDER = '1c4id6My-LmSOZDvTaEHOsf6VpXZSvw0E'
