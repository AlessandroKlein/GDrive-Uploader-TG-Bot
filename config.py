import os

class Config:
  ENV = bool(os.environ.get('ENV', False))
  if ENV:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    APP_ID = os.environ.get('APP_ID')
    API_HASH = os.environ.get('API_HASH')
    DATABASE_URL = os.environ.get('DATABASE_URL')
  else:
    BOT_TOKEN = '1394534244:AAHbVTthzn1sNbclrt9lyrrSt_Msvz46jWA' # Get it from https://t.me/BotFather
    APP_ID = '1680362' # Get it from my.telegram.org/apps
    API_HASH = '8cebfa99b9719c28a5e16fedaa0eeaad' # Get it from my.telegram.org/apps
    DATABASE_URL = 'postgres://mdvgqgverqgesc:263a6b5b49f8539c4b1bb106ff7b300e5b5ebb3b46c3314fc57e8da9865c6457@ec2-34-192-122-0.compute-1.amazonaws.com:5432/d6c18273hu4a0r' # SQL Database URL / Heroku Postgres URL


class Messages:

    START_MSG = "**Hola {}.**\n__Soy Google Drive Uploader Bot. Puedes usarme para cargar cualquier archivo / video a Google Drive desde un enlace directo o archivos de Telegram..__\n__Puedes saber más de /help.__"

    HELP_MSG = [
        ".",
        "**Cargador de Google Drive**\n__Puedo cargar archivos desde un enlace directo o archivos de Telegram a su Google Drive. Todo lo que necesito es autenticarme en su cuenta de Google Drive y enviar un enlace de descarga directa o un archivo de Telegram.__\n\nITengo más funciones ...! ¿Quieres saberlo? Simplemente recorra este tutorial y lea los mensajes con atención.",
        
        "**Autenticar Google Drive**\n__Envía el /auth comando y recibirá una URL, visite URL y siga los pasos y envíe el código recibido aquí. Utilizar /revoke para revocar su cuenta de Google Drive actualmente registrada.__",
        
        "**Enlaces directos**\n__Envíeme un enlace de descarga directa para un archivo, lo descargaré en mi servidor y lo subiré a su cuenta de Google Drive. Puede cambiar el nombre de los archivos antes de cargarlos en la cuenta de GDrive. Solo envíeme la URL y el nuevo nombre de archivo separados por ' | '.__\n\n**__Ejemplos de:__**\n```https://example.com/AFileWithDirectDownloadLink.mkv | Nuevo FileName.mkv```",
        
        "**Archivos de Telegram**\n__Para cargar archivos de telegram en su cuenta de Google Drive, simplemente envíeme el archivo y lo descargaré y lo subiré a su cuenta de Google Drive. Nota: La descarga de archivos de Telegram es lenta. puede llevar más tiempo para archivos grandes.__",
        
        "**Carpeta personalizada para subir**\n__Quiere cargar en una carpeta personalizada o en__ **TeamDrive** __ ?\nUtiliza /setfolder {Folder ID / TeamDrive ID / Folder UrL} para configurar una carpeta de carga personalizada.\nTodos los archivos se cargan en la carpeta personalizada que proporcionas..__",
        
        "**Copiar archivos de Google Drive**\n__Sí, clonar o copiar archivos de Google Drive.\nUtiliza /copy {File id / Folder id or URL} para copiar archivos de Google Drive en su cuenta de Google Drive.__",
        
        "**Reglas y precauciones**\n__1. No copie GRANDES archivos / carpetas de Google Drive. Puede colgar el bot y sus archivos pueden dañarse.\n2. Envíe una solicitud a la vez a menos que el bot detenga todos los procesos.\n3. No envíe enlaces lentos @transfiéralo primero.\n4. No utilice mal, sobrecargue ni abuse de este servicio gratuito.__",
        
        "**Desarrollado por @**"
        ]
