import os
import re
import json
from pyrogram import Client, Filters
from helpers import gDrive_sql as db
from plugins.main import humanbytes
from plugins.token import getIdFromUrl
from helpers import parent_id_sql as sql
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
G_DRIVE_FILE_LINK = "https://drive.google.com/open?id={}"
G_DRIVE_FOLDER_LINK = "https://drive.google.com/drive/folders/{}"



def getFilesByFolderId(service, folder_id):
    page_token = None
    q = f"'{folder_id}' in parents"
    files = []
    while True:
        response = service.files().list(supportsTeamDrives=True,
                                               includeTeamDriveItems=True,
                                               q=q,
                                               spaces='drive',
                                               pageSize=200,
                                               fields='nextPageToken, files(id, name, mimeType,size)',
                                               pageToken=page_token).execute()
        for file in response.get('files', []):
            files.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files


def copyFile(service, file_id, dest_id):
    body = {
        'parents': [dest_id]
    }

    try:
        res = service.files().copy(supportsAllDrives=True,fileId=file_id,body=body).execute()
        return res
    except HttpError as err:
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
            if reason == 'userRateLimitExceeded' or reason == 'dailyLimitExceeded':
               return 'LimitExceeded'
            else:
               return 'error'


def cloneFolder(service, name, local_path, folder_id, parent_id, transferred_size):
    files = getFilesByFolderId(service, folder_id)
    new_id = None
    if len(files) == 0:
        return parent_id
    for file in files:
        if file.get('mimeType') == G_DRIVE_DIR_MIME_TYPE:
            file_path = os.path.join(local_path, file.get('name'))
            current_dir_id = create_directory(service, file.get('name'), parent_id)
            new_id = cloneFolder(service, file.get('name'), file_path, file.get('id'), current_dir_id)
        else:
            try:
                transferred_size += int(file.get('size'))
            except TypeError:
                pass
            try:
                copyFile(service, file.get('id'), parent_id)
                new_id = parent_id
            except Exception as e:
                return 'error'
    return new_id, transferred_size

def create_directory(service, directory_name, parent_id):
        file_metadata = {
            "name": directory_name,
            "mimeType": G_DRIVE_DIR_MIME_TYPE
        }
        if parent_id is not None:
            file_metadata["parents"] = [parent_id]
        file = service.files().create(supportsTeamDrives=True, body=file_metadata).execute()
        file_id = file.get("id")
        return file_id



@Client.on_message(Filters.private & Filters.incoming & Filters.command(['copy']))
async def _copy(client, message):
  creds = db.get_credential(message.from_user.id)
  if creds is None:
    await message.reply_text('❗ **No es un usuario autorizado.**\n__Autorice su cuenta de Google Drive ejecutando /auth Comando para usar este bot.__', quote=True)
    return
  if sql.get_id(message.from_user.id):
    parent_id = sql.get_id(message.from_user.id).parent_id
  else:
    parent_id = 'root'
  transferred_size = 0
  if len(message.command) > 1:
    sent_message = await message.reply_text('**Comprobando el enlace de Google Drive...**', quote=True)
    file_id = getIdFromUrl(message.command[1])
    if file_id == 'NotFound':
      await sent_message.edit('❗ **URL de Google Drive no válido**\n__Solo se pueden copiar los enlaces de Google Drive.__')
      return
    else:
      await sent_message.edit(f'🗂️ **Clonación en Google Drive...**\n__{file_id}__')
    service = build(
        "drive",
        "v3",
        credentials=creds,
        cache_discovery=False
      )
    try:
      meta = service.files().get(supportsAllDrives=True, fileId=file_id, fields="name,id,mimeType,size").execute()
    except HttpError as err:
      if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
            if 'notFound' in reason:
               await sent_message.edit('❗**ERROR: ARCHIVO NO ENCONTRADO**\n__Asegúrese de que el archivo exista y que la cuenta que haya autenticado pueda acceder a él..__')
            else:
               await sent_message.edit(f"**ERROR:** ```{str(err).replace('>', '').replace('<', '')}```")
    except Exception as e:
      await sent_message.edit(f"**ERROR:** ```{str(e).replace('>', '').replace('<', '')}```")
    if meta.get("mimeType") == G_DRIVE_DIR_MIME_TYPE:
       dir_id = create_directory(service, meta.get('name'), parent_id)
       try:
         result, transferred_size = cloneFolder(service, meta.get('name'), meta.get('name'), meta.get('id'), dir_id, transferred_size)
         await sent_message.edit(f"✅ **Copiado exitosamente.**\n[{meta.get('name')}]({G_DRIVE_FOLDER_LINK.format(dir_id)}) __({humanbytes(transferred_size)})__")
       except Exception as e:
         await sent_message.edit(f'**ERROR:** ```{e}```')
    else:
      try:
         file = copyFile(service, meta.get('id'), parent_id)
         await sent_message.edit(f"✅ **Copiado exitosamente.**\n[{file.get('name')}]({G_DRIVE_FILE_LINK.format(file.get('id'))}) __({humanbytes(int(meta.get('size')))})__")
      except Exception as e:
         await sent_message.edit(f'**ERROR:** ```{e}```')
  else:
    await message.reply_text('**Copiar archivos o carpetas de Google Drive**\n__Copie los archivos / carpetas de GDrive en su cuenta de Google Drive. Utilizar__ ```/copy {GDriveFolderURL/FileURL}``` __para copiar.__')
