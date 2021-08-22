# Bot de Telegram Uploader de Google Drive
** Un bot de Telegram asyncio para cargar archivos desde Telegram o enlaces directos a Google Drive. **
- Encuéntrelo en Telegram como [Google Drive Uploader] (https://t.me/uploadgdrivebot)

## Características
- [X] Soporte de archivos de Telegram.
- [X] Soporte de enlaces directos.
- [X] Carpeta de carga personalizada.
- [X] Soporte TeamDrive.
- [X] Clonar / Copiar archivos de Google Drive.

## Que hacer
- [] Maneja más excepciones.
- [] Soporte LOGGER.
- [] Soporte de cuenta de servicio.

## Implementación

### Instalación
- Clona este repositorio de git.
```sh 
git clone https://github.com/AlessandroKlein/GDrive-Uploader-TG-Bot
```
- Cambio de directorio
```sh 
cd gdrive-uploader-telegram-bot
```
- Instalar requisitos con pip3
```sh 
pip3 install -r requirements.txt
```

### Configuración
** Hay dos formas de configurar este bot. **
- Add [APP_ID](https://my.telegram.org/apps), [API_HASH](https://my.telegram.org/apps), [BOT_TOKEN](https://t.me/BotFather), DATABASE_URL, ENV in Environment Variables.
- Add [APP_ID](https://my.telegram.org/apps), [API_HASH](https://my.telegram.org/apps), [BOT_TOKEN](https://t.me/BotFather), DATABASE_URL in [config.py](./config.py)

## Implementar
- Implementar en VPS.
```sh 
python3 bot.py
```
## Implementar en Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AlessandroKlein/GDrive-Uploader-TG-Bot)

- Nota: Bot está en fase beta. Quizás arroje algunos errores.

## Créditos
- [Dan](https://github.com/delivrance) for [PyroGram](https://pyrogram.org)
- [Spechide](https://github.com/Spechide) for [gDrive_sql.py](./helpers/gDrive_sql.py)
- [Shivam Jha](https://github.com/lzzy12) for [python-aria-mirror-bot](https://github.com/lzzy12/python-aria-mirror-bot)

## :clap:  Supporters
[![Stargazers repo roster for @cdfxscrq/gdrive-uploader-telegram-bot](https://reporoster.com/stars/cdfxscrq/gdrive-uploader-telegram-bot)](https://github.com/cdfxscrq/gdrive-uploader-telegram-bot/stargazers)
[![Forkers repo roster for @cdfxscrq/gdrive-uploader-telegram-bot](https://reporoster.com/forks/cdfxscrq/gdrive-uploader-telegram-bot)](https://github.com/cdfxscrq/gdrive-uploader-telegram-bot/network/members)
