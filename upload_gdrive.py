from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


gauth = GoogleAuth()

def authentication():
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")


def upload_file(file_path):

    try:
        drive = GoogleDrive(gauth)
        file_name = file_path.split(os.sep)[-1]
        my_file = drive.CreateFile({'parents': [{'id': '1c4id6My-LmSOZDvTfEHOsf6VpXZSvw0E'}]})
        my_file.SetContentFile(file_path)
        my_file.Upload()

        return f'\nFile {file_name} was uploaded successfully!'

    except Exception as ex:
        print(ex)


def main():
    authentication()
    print(upload_file('test.txt'))


if __name__ == '__main__':
    main()