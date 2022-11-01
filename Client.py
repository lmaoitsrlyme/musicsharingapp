import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib
import os
import ntpath 
import time
from ftplib import FTP
from tkinter import filedialog
from pathlib import Path
import winsound
from playsound import playsound
import pygame
from pygame import mixer

PORT  = 8050
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096

name = None
listbox =  None
filePathLabel = None

global song_counter
song_counter = 0


def browseFiles():
    global listbox
    global song_counter
    global filePathLabel

    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname=ntpath.basename(filename)
        with open(filename, 'rb') as file:
            ftp_server.storbinary(f"STOR {fname}", file)

        ftp_server.dir()
        ftp_server.quit()
       
        listbox.insert(song_counter, fname)
        song_counter = song_counter + 1
        
    except FileNotFoundError:
        print("cancel")


def play():
    global selected_song
    selected_song = listbox.get(ANCHOR)
    
    pygame
    mixer.init()
    mixer.music.load('shared_files/' + selected_song)
    mixer.music.play()
    if(selected_song != ""):
       infoLabel.configure(text = "now playing this slay song: " +selected_song)
    else:
       infoLabel.configure(text = "")

def stop():
    global selected_song
    pygame
    mixer.init()
    mixer.music.load('shared_files/' + selected_song)
    mixer.music.pause()
    infoLabel.configure(text = "")
    
def pause():
    global selected_song
    pygame
    mixer.init()
    mixer.music.load('shared_files/' + selected_song)
    mixer.music.pause()

def resume():
    global selected_song
    mixer.init()
    mixer.music.load('shared_files/' + selected_song)
    mixer.music.play() 
   
  
def download():    
    song_to_download=listbox.get(ANCHOR)
    infoLabel.configure(text = "currently downloading "+ song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home = str(Path.home())
    download_path = home + "/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, 'wb')
    ftp_server.retrbinary('RETR '+ song_to_download, file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text = "completed downloading" + selected_song)
    time.sleep(1)
    if(selected_song != ""):
        infoLabel.configure(text = "currently playing: " + selected_song)
    else:
       infoLabel.configure(text = "") 
   
def musicWindow(): 
    global song_counter
    global filePathLabel
    global listbox
    global infoLabel
    
    window=Tk()
    window.title('spotify ripoff')
    window.geometry("300x300")
    window.configure(bg = '#f4a9bb')
    
    selectlabel = Label(window, text = "select song",bg = '#f4a9bb', font = ("Helvetica", 8))
    selectlabel.place(x = 2, y = 1)
    
    listbox = Listbox(window,height = 10, width = 39, activestyle = 'dotbox', bg = '#f4a9bb', borderwidth = 2, font = ("Helvetica", 10))
    listbox.place(x = 10, y = 18)
    for file in os.listdir('shared_files'):
        filename = os.fsdecode(file)
        listbox.insert(song_counter, filename)
        song_counter = song_counter + 1
        
    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)
    
    playbtn = Button(window, text = "slay (play)", width = 10, bd = 1, bg = 'LightSkyBlue', font = ("Helvetica", 10), command = play)
    playbtn.place(x = 30, y = 200)
    
    stopbtn = Button(window, text = "stop", bd = 1, width = 10, bg = 'LightSkyBlue', font = ("Calibri",10), command = stop)
    stopbtn.place(x = 200, y = 200)
    
    resumebtn = Button(window,text = "resume", width = 10, bd = 1, bg = 'LightSkyBlue', font = ("Calibri", 10), command = resume)
    resumebtn.place(x = 30, y = 250)

    pausebtn = Button(window,text = "pause", width = 10, bd = 1, bg = 'LightSkyBlue', font = ("Calibri", 10), command = pause)
    pausebtn.place(x = 200, y = 250)

    
    uploadbtn = Button(window, text = "upload", width = 10, bd = 1, bg = 'SkyBlue', font = ("Calibri", 10), command = browseFiles)
    uploadbtn.place(x = 30, y = 250)
    
    downloadbtn = Button(window, text = "download", width = 10, bd = 1, bg = 'SkyBlue', font = ("Calibri", 10), command = download)
    downloadbtn.place(x = 200, y = 250)
    
    informationlabel = Label(window, text = "", fg = "blue", bg = 'SkyBlue', font = ("Calibri",8))
    informationlabel.place(x = 4, y = 280)
    
    window.mainloop()
    
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS
    global song_counter

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    musicWindow()

setup()