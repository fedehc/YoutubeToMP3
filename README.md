# YoutubeToMP3 1.0b

Una simple app de escritorio que hace de frontend del programa *youtube_dl* y que permite descargar música en formato MP3 desde Youtube mismo.

Creado con *Python 3*, usando *Tkinter* para la interfaz gráfica y *Youtube_dl* para descargar y convertir los videos a MP3 (usando *FFmpeg* internamente para la conversión de video a audio).

![Imagen](https://github.com/FedeHC/YoutubeToMP3/blob/master/images/captura-1.jpg)

## Aclaraciones:
- De momento no es más que un script ejecutable, solo probado en Linux Mint 18/19. Faltaría testear en otras distros ¡y en Windows y Mac! Aunque en principio debería correr sin problemas en cualquiera de estos (o con pequeñas correcciones) si se cumplen con los requisitos.

## Requisitos:
- [Python 3.5 (o superior)](https://www.python.org/downloads/).
    - El módulo **Tkinter** suele venir por defecto con *Python*, pero si surgen problemas chequear que [esté correctamente instalado](https://tkdocs.com/tutorial/install.html) en nuestro SO.

- Tener instalado [Youtube_dl](http://ytdl-org.github.io/youtube-dl/download.html).
    - En Windows se necesita instalar [Microsoft Visual C++ 2010 Redistributable Package (x86)](https://www.microsoft.com/en-US/download/details.aspx?id=5555) (más detalles en [Youtube_dl](http://ytdl-org.github.io/youtube-dl/download.html)).
    - En cualquier SO, se necesita tener instalado [FFmpeg](https://ffmpeg.org/download.html) para que Youtube_dl pueda efectuar la conversión de video a MP3.

- En Linux es recomendable usar [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/) para instalar *Python 3* por separado de la versión que utilize internamente el SO.

## Uso:
Simplemente ejecutar el script de python:
```
    python3 YouTubeToMP3.py
```

Para descargar música, basta con copiar y pegar la url del video y elegir una carpeta de destino:

![Imagen](https://github.com/FedeHC/YoutubeToMP3/blob/master/images/captura-2.jpg)


### Más info:
- [Python Doc](https://www.python.org/doc/)
- [Youtube_dl Doc](https://github.com/ytdl-org/youtube-dl/blob/master/README.md)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html/)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)