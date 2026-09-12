import os
import sys

import tkinter as tk
from tkinter import filedialog as fd, messagebox as msg

from pathlib import Path
from yt_dlp import YoutubeDL

def add_bundled_tools_to_path():
    if getattr(sys, "frozen", False):
        tools_folder = Path(sys._MEIPASS)
        os.environ["PATH"] = (
            f"{tools_folder}{os.pathsep}{os.environ['PATH']}"
        )


add_bundled_tools_to_path()


def download_video():
    link = link_entry.get().strip() #strip removes any spaces or blank lines accidentally pasted in

    if not link:
        msg.showwarning("Missing a link", "Paste a YouTube link to download the video.")
        return

    folder = fd.askdirectory(title="Select a folder to save the video")

    if not folder:
        return

    try:
        options = {
            "format": "bestvideo*+bestaudio/best", #Prefers the best available video in mp4 format, if not available choose the next best format
            "noplaylist" : True, #if link is a playlist, downloads only that video, not whole playlist
            "outtmpl": str(Path(folder) / "%(title)s.%(ext)s"), #filename template fot chosen save folder, both title and extension
            
        }

        with YoutubeDL(options) as downloader:
            downloader.download([link])

            msg.showinfo("Download completed successfully", "Video downloaded successfully. Check selected save folder")

    except Exception as error:
        msg.showerror("Error occured while downloading the video", str(error))


app = tk.Tk()
app.title("YoutTube Downloader")
app.geometry("500x300") #defines the size of the application window

heading = tk.Label(
    app,
    text="YouTube Downloader",
    font=("Oswald", 22, "bold"),

)

heading.pack(pady=35) #places the message in the app window with a padding of 35 pixels from the top

link_label = tk.Label(app, text="Paste the YouTube link below:", font=("Oswald", 14))
link_label.pack()

link_entry = tk.Entry(app, width=60)
link_entry.pack(pady=10)

download_button = tk.Button(app, text="Download video", font=("Oswald", 14), command=download_video)
download_button.pack(pady=20)

app.mainloop()
