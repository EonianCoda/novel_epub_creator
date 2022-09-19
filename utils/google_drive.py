from __future__ import print_function

import os

from utils.config import Setting, GOOGLE_DRIVE_PATH

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from utils.database import Database

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
SETTING = Setting()


def search_folder(service, update_drive_folder_name=None):
    """
    如果雲端資料夾名稱相同，則只會選擇一個資料夾上傳，請勿取名相同名稱
    :param service: 認證用
    :param update_drive_folder_name: 取得指定資料夾的id, 沒有的話回傳None, 給錯也會回傳None
    """

    get_folder_id_list = []
    if update_drive_folder_name is not None:
        response = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive',
                                       q = "name = '" + update_drive_folder_name + "' and mimeType = 'application/vnd.google-apps.folder' and trashed = false").execute()

        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            get_folder_id_list.append(file.get('id'))

        if len(get_folder_id_list) == 0:
            print("你給的資料夾名稱沒有在你的雲端上！，因此檔案會上傳至雲端根目錄")
            return None
        else:
            return get_folder_id_list

    return None
def update_file(service, update_drive_service_name, local_file_path, update_drive_service_folder_id):
    """
    將本地端的檔案傳到雲端上
    :param service: 認證用
    :param update_drive_service_name: 存到 雲端上的名稱
    :param local_file_path: 本地端的位置
    :param local_file_name: 本地端的檔案名稱
    """

    print("正在上傳檔案...")
    if update_drive_service_folder_id is None:
        file_metadata = {'name': update_drive_service_name}
    else:
        print("雲端資料夾id: %s" % update_drive_service_folder_id)
        file_metadata = {'name': update_drive_service_name,
                         'parents': update_drive_service_folder_id}
    media = MediaFileUpload(local_file_path, )
    file_metadata_size = media.size()
    file_id = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("上傳檔案成功！")
    print('雲端檔案名稱為: ' + str(file_metadata['name']))
    print('雲端檔案ID為: ' + str(file_id['id']))
    print('檔案大小為: ' + str(file_metadata_size) + ' byte')
    return file_metadata['name'], file_id['id']
def get_creds():
    creds = None
    token_path = './.keys/token.json'
    cred_path = './.keys/credentials.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds
def get_file_list(service):
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    return items
def file_exist(items,filename):
    item_list=[]
    for item in items:
        item_list.append(item['name'])
    if filename in item_list:
        return True
    else :
        return False 
def upload(file, local_file_path):
    """
    建立service並將本地端的檔案傳到雲端上
    :file:(上傳的檔案名稱,資料來源)
    :local_file_path:檔案位置
    """
    creds = get_creds()
    database = Database()
    filename,source_idx = file
    try:
        service = build('drive', 'v3', credentials=creds)
        item_list=[]
        items = get_file_list(service=service)
        for item in items:
            item_list.append(item['name'])
        
        get_folder_id = search_folder(service = service, 
                                        update_drive_folder_name = 'Novel')
        items = get_file_list(service=service)
        if filename not in item_list:
            file_name,file_id = update_file(service=service,update_drive_service_name=filename,local_file_path=local_file_path,update_drive_service_folder_id=get_folder_id)
            path = GOOGLE_DRIVE_PATH.format(file_id)
            key = str((filename,source_idx))
            if database.get_download(key)== None:
                database.add_download(key,file_id)
            return path
        else :
            # print('same')
            file_id = items[item_list.index(filename)]['id']
            key = str((filename,source_idx))
            if database.get_download(key)== None:
                database.add_download(key,file_id)
            path =GOOGLE_DRIVE_PATH.format(items[item_list.index(filename)]['id'])
            return path
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')
if __name__ =='__main__':
    name = str(29295)
    print(upload(filename=name+'.epub',local_file_path= SETTING.get_OUTPUT_PATH(name)))

