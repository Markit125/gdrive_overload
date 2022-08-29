from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from dotenv import load_dotenv
import time

load_dotenv()
GDRIVE_FOLDER = os.getenv('GDRIVE_FOLDER')

gauth = GoogleAuth()


def authentication():
    gauth.LoadCredentialsFile("mycreds.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.json")


def download_log_file(folder):
    try:
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()

        for file in file_list:
            if 'log.txt' in file['title']:
                file.GetContentFile(file['title'])
                return True
        return False
    except Exception as ex:
        print(ex)


def main():
    authentication()
    old_length = 0
    while True:
        if download_log_file(GDRIVE_FOLDER):
            with open('log.txt', 'r') as log:
                text = log.readlines()
                length = len(text)

                if length == old_length:
                    continue

                os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                print(*text[old_length:])

                if 'successfully!' in text[-1]:
                    os.remove('log.txt')
                    return

                old_length = length

            time.sleep(15)
        else:
            time.sleep(5)


if __name__ == '__main__':
    main()