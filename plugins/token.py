import re
from httplib2 import Http
from pyrogram import Client, Filters
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from helpers import gDrive_sql as db
from helpers import parent_id_sql as sql

OAUTH_SCOPE = "https://www.googleapis.com/auth/drive"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
G_DRIVE_CLIENT_ID = "197036948433-4sjgjrj1osm5b5neu8khh7c2nsvn96f7.apps.googleusercontent.com"
G_DRIVE_CLIENT_SECRET = "dnXoMIu2V7HQ8G8RicrKmvlu"
flow = None

@Client.on_message(Filters.private & Filters.incoming & Filters.command(['auth']))
async def _auth(client, message):
  creds = db.get_credential(message.from_user.id)
  if creds is not None:
    creds.refresh(Http())
    db.set_credential(message.from_user.id, creds)
    await message.reply_text("🔒 **Ya autorizó su cuenta de Google Drive.**\n__Use /revoke para revocar la cuenta corriente.__\n__Envíeme un enlace directo o un archivo para cargar en Google Drive__", quote=True)
  else:
    global flow
    try:
      flow = OAuth2WebServerFlow(
              G_DRIVE_CLIENT_ID,
              G_DRIVE_CLIENT_SECRET,
              OAUTH_SCOPE,
              redirect_uri=REDIRECT_URI
      )
      auth_url = flow.step1_get_authorize_url()
      await client.send_message(message.from_user.id, "⛓️ **Para autorizar su cuenta de Google Drive, visite esta [URL] ({}) y envíe el código generado aquí..**\n__Visite la URL> Permitir permisos> obtendrá un código> cópielo> Envíelo aquí__".format(auth_url))
    except Exception as e:
      await message.reply_text(f"**ERROR:** ```{e}```", quote=True)


@Client.on_message(Filters.private & Filters.incoming & Filters.command(['revoke']))
async def _revoke(client, message):
  if db.get_credential(message.from_user.id) is None:
   await message.reply_text("🔑 **No me has autenticado para subir a ninguna cuenta.**\n__Enviar /auth autenticar.__", quote=True)
  else:
    try:
      db.clear_credential(message.from_user.id)
      await message.reply_text("🔓 **Cuenta autenticada revocada con éxito.**", quote=True)
    except Exception as e:
      await message.reply_text(f"**ERROR:** ```{e}```", quote=True)


@Client.on_message(Filters.private & Filters.incoming & Filters.command(['setfolder']))
async def _set_parent(client, message):
  if len(message.command) > 1:
    cmd_msg = message.command[1]
    if cmd_msg.lower() == "clear":
      sql.del_id(message.from_user.id)
      await message.reply_text('**ID de carpeta personalizada borrado**\n__Use /setfolder <URL de carpeta> para restablecerla.__', quote=True)
    else:
      file_id = getIdFromUrl(cmd_msg)
      if 'NotFound' in file_id:
        await message.reply_text('❗ URL de carpeta no válida**\n__Copie la identificación de la carpeta personalizada correctamente.__', quote=True)
      else:
        sql.set_id(message.from_user.id, file_id)
        await message.reply_text(f'**El ID de carpeta personalizado se establece correctamente**\n__Su ID de carpeta personalizada establecido en {file_id}. Todas las subidas (desde ahora) va aquí.\nUse__ ```/setfolder clear``` __para borrar el ID de carpeta actual.__', quote=True)
  else:
    if sql.get_id(message.from_user.id):
      await message.reply_text(f'**Su ID de carpeta personalizada es** ```{sql.get_id(message.from_user.id).parent_id}```.', quote=True)
    else:
      await message.reply_text('**No configuró ningún ID de carpeta personalizado**\n__Use__ ```/setfolder {folder URL}``` __para configurar su ID de carpeta personalizada.__', quote=True)

@Client.on_message(Filters.private & Filters.incoming & Filters.text)
async def _token(client, message):
  token = message.text.split()[-1]
  WORD = len(token)
  if WORD == 57 and token[1] == "/":
    creds = None
    global flow
    if flow is None:
        await message.reply_text(
            text="❗ **Codigo invalido**\n__Correr /auth primero.__",
            quote=True
        )
        return
    try:
      m = await message.reply_text(text="**Comprobando el código recibido...**", quote=True)
      creds = flow.step2_exchange(message.text)
      db.set_credential(message.from_user.id, creds)
      await m.edit('**Cuenta de Google Drive autorizada correctamente.**')
      flow = None
    except FlowExchangeError:
      await m.edit('❗ **Codigo invalido**\n__El código que ha enviado no es válido o ya se utilizó antes. Genere uno nuevo por la URL de autorización__')
    except Exception as e:
      await m.edit(f"**ERROR:** ```{e}```")


def getIdFromUrl(link: str):
      found = re.search(
        r'https://drive.google.com/[\w\?\./&=]+([-\w]{33}|(?<=/)0A[-\w]{17})', link)
      if found:
        return found.group(1)
      elif len(link.split()[-1]) == 33 or len(link.split()[-1]) == 19:
        return link
      else:
        return 'NotFound'
