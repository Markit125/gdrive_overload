from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from dotenv import load_dotenv

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


def upload_file(file_path, folder=None):
    authentication()
    try:
        drive = GoogleDrive(gauth)
        file_name = file_path.split(os.sep)[-1]
        if folder != None:
            my_file = drive.CreateFile({'parents': [{'id': f'{folder}'}], 'title': f'{file_path.split("/")[-1]}'})
        else:
            my_file = drive.CreateFile()
        my_file.SetContentFile(file_path)
        my_file.Upload()

        print(f'\nFile {file_name} was uploaded successfully!')

    except Exception as ex:
        print(ex)


def download_file(folder, torrent=False):
    authentication()
    try:
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()

        for file in file_list:
            if ('.torrent' in file['title']) == torrent:
                print(f"{file['title']} is downloading")
                file.GetContentFile(file['title'])
                return True
        return False
    except Exception as ex:
        print(ex)


def main():
    # upload_file(file_path='test1.txt')
    # upload_file(file_path='test.txt', folder='1c4id6My-LmSOZDvTfEHOsf6VpXZSvw0E')
    download_file(folder=GDRIVE_FOLDER, torrent=True)


if __name__ == '__main__':
    main()
