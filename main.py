import os
import sys
import tkinter as tk
import subprocess
import threading
from tkinter import messagebox, ttk
from pytube import YouTube
from pytube import Playlist
from datetime import datetime
import ctypes
import queue


# Set the Windows application ID for taskbar grouping
myappid = 'pieware.YoutubeToMp3.converter.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Set up paths for download folders
DESKTOP_PATH = os.path.expanduser("~\\Desktop")
YT_DOWNLOADS_PATH = os.path.join(DESKTOP_PATH, "yt_downloads")
MP3_PATH = os.path.join(YT_DOWNLOADS_PATH, "mp3")
MP4_PATH = os.path.join(YT_DOWNLOADS_PATH, "mp4")

playlist_queue = queue.Queue()



# Function to display pop-up messages
def throw_popup(title, message, error=True):
    if error:
        messagebox.showerror(title, message)
    else:
        messagebox.showinfo(title, message)


# Function to clear URL entry field
def clear_url_field():
    url_entry.delete(0, tk.END)


# Function to open the file location in the system's file explorer
def open_file_location(download_folder):
    try:
        # Open file location based on the platform
        if sys.platform.startswith('win'):
            subprocess.Popen(['explorer', os.path.normpath(download_folder)])
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', download_folder])
        elif sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', download_folder])
        else:
            throw_popup("Error", "Unsupported platform for opening file location.")
    except Exception:
        throw_popup("Error",
                    "Directory doesn't exist yet but will be created automatically after you download something")


# Function to download media (audio or video) from a given URL
def download_media(url, media_type, format_function, success_message):
    try:
        # Create a YouTube object and get the appropriate stream
        media = YouTube(url)
        stream = format_function(media)

        if stream:
            # Determine the download folder based on media type
            download_folder = MP3_PATH if media_type == "mp3" else MP4_PATH
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            # Generate a unique filename using timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"{media.title}_{timestamp}.{media_type}"

            print(f"Downloading {media_type}: {media.title}")
            stream.download(output_path=download_folder, filename=new_file_name)

            if not playlist_checkbox_var.get():
                throw_popup("Completed successfully", f"{success_message}: {new_file_name}", False)
        else:
            throw_popup("Error", f"No {media_type} stream found for the provided URL")
    except Exception:
        if not playlist_checkbox_var.get():
            throw_popup("Error", "Invalid YouTube URL")


# Function to handle asynchronous download button click
def download_button_click_async(url, download_type):
    global download_in_progress

    if download_in_progress:
        return

    try:
        download_in_progress = True
        download_button.config(state=tk.DISABLED, text="Downloading...")
        playlist_checkbox.config(state="disabled")

        if download_type == "mp3":
            download_media(url, "mp3", lambda media: media.streams.filter(only_audio=True).first(),
                           "Downloaded and converted")
        elif download_type == "mp4":
            download_media(url, "mp4", lambda media: media.streams.get_highest_resolution(), "Downloaded")

    finally:
        download_in_progress = False
        download_button.config(state=tk.NORMAL, text="Download")
        playlist_checkbox.config(state="normal")
        download_status_label.config(text="Download completed")  # Update the status label



def download_playlist(url):
    try:
        playlist = Playlist(url)

        for video in playlist.videos:
            playlist_queue.put(video.watch_url)

    except Exception:
        throw_popup("Error", "Invalid YouTube playlist URL")


def download_playlist_worker(media_type):
    while not playlist_queue.empty():
        video_url = playlist_queue.get()
        download_button_click_async(video_url, media_type)
        playlist_queue.task_done()
        download_status_label.config(text=f"Downloading: {playlist_queue.qsize()} files remaining")
    throw_popup("Playlist", "Downloaded", False)
    download_status_label.config(text="Download completed")  # Update the status label after playlist download


# Function to handle download button click
def on_download_button_click():
    url = url_entry.get()
    if url:
        download_type = download_type_var.get()
        if playlist_checkbox_var.get():
            download_playlist(url)
            threading.Thread(target=download_playlist_worker, args=(download_type,)).start()
        else:
            threading.Thread(target=download_button_click_async, args=(url, download_type)).start()



# Create the main GUI window
root = tk.Tk()  # Window
root.title("YouTube To Mp[3,4]")
root.geometry("730x550")
root.minsize(730, 550)
root.configure(bg="#292929")

# Set up the style for GUI elements
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12, "bold"), background="#292929", foreground="#84C9Fb")
style.configure("TButton", font=("Helvetica", 12), background="#000000", foreground="#000000",
                borderwidth=0, focuscolor="#292929")
style.map("TButton",
          background=[("active", "#84C9Fb"), ("disabled", "#555555")],
          foreground=[("active", "#292929")])
style.configure("TEntry", font=("Helvetica", 12), background="white", foreground="#000000")

# Create and place GUI elements
url_label = ttk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=(15, 0))

# Create the urlFrame with the entry and the download type
input_frame = ttk.Frame(master=root)
url_entry = ttk.Entry(master=input_frame, width=40)
# Create a radio buttons for selecting download type
download_type_var = tk.StringVar(value="mp3")
mp3_radio_button = ttk.Radiobutton(input_frame, text="MP3", variable=download_type_var, value="mp3")
mp4_radio_button = ttk.Radiobutton(input_frame, text="MP4", variable=download_type_var, value="mp4")

url_entry.pack(side='left')
mp3_radio_button.pack(side='left')
mp4_radio_button.pack()
input_frame.pack(pady=5)


# Create a variable to store the state of the checkbox
playlist_checkbox_var = tk.IntVar()
playlist_checkbox = tk.Checkbutton(root, text="Playlist", variable=playlist_checkbox_var)
playlist_checkbox.pack(pady=5)

# Create download button
download_button = ttk.Button(root, text="Download", command=on_download_button_click)
download_button.pack(pady=(10, 0))

# Create the Clear button to clear the URL entry
clear_button = ttk.Button(root, text="Clear", command=clear_url_field)
clear_button.pack(pady=(10, 0))


download_status_label = ttk.Label(root, text="", font=("Helvetica", 10))
download_status_label.pack(pady=(10, 50))



# Initialize the download_in_progress flag
download_in_progress = False

# Define download type labels
download_type_labels = {"mp3": "Downloaded mp3 files will be saved in:",
                        "mp4": "Downloaded mp4 files will be saved in:"}

# Create and display the destination folder labels
for download_type, label_text in download_type_labels.items():
    destination_label_text = f"{label_text} {MP3_PATH}" if download_type == "mp3" else f"{label_text} {MP4_PATH}"
    destination_label = ttk.Label(root, text=destination_label_text)
    destination_label.pack(pady=(10, 0))

    # Create the "Show" button to open the file location
    show_button = ttk.Button(root, text=f"Show {download_type} download Folder",
                             command=lambda dt=download_type: open_file_location(
                                 os.path.expanduser(MP3_PATH if dt == "mp3" else MP4_PATH)))
    show_button.pack(pady=(10, 25))

# Start the GUI event loop
root.mainloop()
