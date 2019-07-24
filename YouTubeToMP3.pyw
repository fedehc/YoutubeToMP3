#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# P/ Youtube_dl (si o si tiene que ser 1° linea de código):
from __future__ import unicode_literals

try:
  # Youtube_dl:
  import youtube_dl

  # Tkinter:
  from tkinter import *

  # Otros:
  import os

except ImportError as e:
  print("\n[ERROR al cargar módúlos necesarios para el programa.\nDetalles del error:\n")
  print(e)


class YoutubeToMP3():
  """Clase para GUI de Tkinter."""
  def __init__(self, dirFinal, template="%(title)s.%(ext)s"):

    # Variable estado de la descarga:
    self.downloadStatus = None

    # El nombre del archivo mp3:
    self.mp3file = ""

    # Obteniendo directorio actual de trabajo (para usar como carpeta temporal de trabajo):
    self.dirTemp = os.getcwd() + "/"

    # Carpeta de descarga:
    self.dirFinal = dirFinal

    # El nombre y la extensión final al mp3 convertido (el nombre original del video + .mp3):
    self.template = template

    # Diccionario con la configuración para la conversión del video a mp3 con youtube_dl.
    # (https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl)
    self.ytdl_opts = {
      "format": "bestaudio/best",
      "postprocessors": [{
          "key": "FFmpegExtractAudio",
          "preferredcodec": "mp3",
          "preferredquality": "320",
      }],
      "logger": MyLogger(),
      "progress_hooks": [self.my_hook],
      "outtmpl": self.template,
    }

    # Iniciando interfaz gráfica:
    self.gui()


  def gui(self):
    """Método que inicia la interfaz gráfica del programa con sus respectivos widgets."""
    self.window = Tk()
    self.window.title("YouTubeToMP3")
    self.window.geometry("700x120")
    self.window.resizable(0, 0)

    # [Logo del programa]
    self.image = Image("photo", file="images/logo.png")
    self.window.tk.call("wm", "iconphoto", self.window._w, self.image)

    # [URL]
    self.lbURL = Label(self.window, text="Youtube URL:", font=("Arial", 14))
    self.lbURL.grid(column=0, row=0, padx=10, pady=10, sticky=W,)

    self.enURL = Entry(self.window, width=41, font=("Arial", 14), fg="red", bd=0,
                  highlightcolor="#EF5958", highlightthickness=1, selectbackground="#EF5958")
    self.enURL.grid(column=1, row=0, sticky=W)
    self.enURL.focus()

    # [Carpeta de Descarga]
    self.lbDir = Label(self.window, text="Carpeta de descarga:", font=("Arial", 10))
    self.lbDir.grid(column=0, row=1, padx=10, sticky=W)

    self.enDir = Entry(self.window, width=64, font=("Arial", 10), bd=0, selectbackground="#EF5958")
    self.enDir.insert(0, self.dirFinal)
    self.enDir.grid(column=1, row=1, sticky=W)

    # [Carpeta temporal]
    self.lbTemp = Label(self.window, text="Carpeta temporal:", font=("Arial", 10))
    self.lbTemp.grid(column=0, row=2, padx=10, sticky=W)

    self.enTemp = Entry(self.window, width=64, font=("Arial", 10), bd=0, selectbackground="#EF5958")
    self.enTemp.insert(0, self.dirTemp)
    self.enTemp.grid(column=1, row=2, sticky=W)

    # [Status]
    self.lbStatusTitle = Label(self.window, text="Status:", font=("Arial", 10))
    self.lbStatusTitle.grid(column=0, row=3, padx=10, sticky=W)

    self.lbStatus = Label(self.window, text="Esperando una URL válida...",
                     font=("Arial", 10, "italic"))
    self.lbStatus.grid(column=1, row=3, pady=10, sticky=W)


    self.btnDownload = Button(self.window, text="Iniciar!", font=("Arial", 10), command=self.downloadAndConvert)
    self.btnDownload.grid(column=2, row=0, padx=10, sticky=W)

    # Iniciando Tkinter loop:
    self.window.mainloop()

    return


  def checkURL(self, url):
    """Método que chequea si la url de youtube pasada por argumento es válida."""
    if url == "":
      return False, "vacio"

    elif url.startswith("https://www.youtube.com/watch?v=") or url.startswith("www.youtube.com/watch?v="):
      if "&" in url:
        pos = url.find("&")
        goodURL = url[0:pos]
        if url.startswith("https://"):
          return True, goodURL
        else:
          return True, "https://" + goodURL
      else:
        return True, url

    else:
      return False, "inválido"


  def downloadAndConvert(self):
    """Método que procede a descargar el video, convertirlo a MP3 y moverlo a la carpeta de destino especificado."""
    
    # Obteniendo la info de todos los campos:
    url = self.enURL.get()
    self.dirFinal = self.enDir.get()
    self.dirTemp = self.enTemp.get()

    # Chequear URL:
    validURL, statusURL = self.checkURL(url)
    
    if not validURL:
      if statusURL == "vacio":
        self.lbStatus.configure(text="URL vacia, ingrese una.", fg="red")
      else:
        self.lbStatus.configure(text="URL no válida, ingrese una nueva.", fg="red")

      self.enURL.select_range(0, END) # Dejar seleccionado el campo enURL.

    
    # Si está bien la URL se continua:
    else:
      # Cambiando a la URL ya rectificada:
      url = statusURL

      # Llamando a youtube_dl para descargar video y convirtir a mp3:
      self.ytdl_convert(url)

      # Si terminó la descarga y la conversión a mp3, renombrar y mover a la carpeta destino:
      if self.downloadStatus == "descargado":
        oldname = self.mp3file
        self.mp3file = self.mp3file .replace(" - ", "- ")
        os.rename(self.dirTemp + oldname, self.dirFinal + self.mp3file)

    return


  def ytdl_convert(self, url):
    """Método que invoca youtube_dl para realizar la descarga y la conversión."""
    with youtube_dl.YoutubeDL(self.ytdl_opts) as ytdl:
        ytdl.download([url])

    return


  def my_hook(self, d):
    """Método para recibir mensaje de éxito desde youtube_dl."""
    if d["status"] == "error":
      self.downloadStatus = "error"
      self.lbStatus.configure(text="Error al intentar descargar video desde Youtube.", fg="red")

    if d["status"] == "downloading":
      self.downloadStatus = "descargando"
      self.btnDownload.config(state='disabled')   # Desactivando temp. el botón de iniciar (para evitar problemas).
      self.lbStatus.configure(text="Iniciando descarga, por favor espere...", fg="green")

    if d["status"] == "finished":
      self.downloadStatus = "descargado"
      self.mp3file = d["filename"]                # Nombre video + extensión original.
      pos = self.mp3file .find(".")               # Buscando donde empieza la extensión.
      self.mp3file = self.mp3file[0:pos] + ".mp3" # Borrando vieja extensión y cambiando por ".mp3"

      self.btnDownload.config(state='normal')     # Activando nuevamente el botón de iniciar descarga.
      self.lbStatus.configure(text="Descarga y conversión completa! (chequear en carpeta destino)", fg="green")

    return


class MyLogger(object):
  """Clase para poder recibir mensajes de error desde youtube_dl."""

  def debug(self, msg):
    pass

  def warning(self, msg):
    pass

  def error(self, msg):
    print(msg)


# Iniciando:
if __name__ == '__main__':
  youtubeToMp3 = YoutubeToMP3("/media/Archivos/")
