import os
import sys
import tkinter as tk
import subprocess
import threading
from tkinter import messagebox, ttk
from pytube import YouTube
from datetime import datetime
import ctypes

# Set the Windows application ID for taskbar grouping
myappid = 'pieware.YoutubeToMp3.converter.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Set up paths for download folders
DESKTOP_PATH = os.path.expanduser("~/Desktop")
YT_DOWNLOADS_PATH = os.path.join(DESKTOP_PATH, "yt_downloads")
MP3_PATH = os.path.join(YT_DOWNLOADS_PATH, "mp3")
MP4_PATH = os.path.join(YT_DOWNLOADS_PATH, "mp4")


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

            throw_popup("Completed successfully", f"{success_message}: {new_file_name}", False)
        else:
            throw_popup("Error", f"No {media_type} stream found for the provided URL")
    except Exception:
        throw_popup("Error", "Invalid YouTube URL")


# Function to handle asynchronous download button click
def download_button_click_async(url, download_type):
    global download_in_progress

    if download_in_progress:
        return

    try:
        download_in_progress = True
        download_button.config(state=tk.DISABLED, text="Downloading...")

        if download_type == "mp3":
            download_media(url, "mp3", lambda media: media.streams.filter(only_audio=True).first(),
                           "Downloaded and converted")
        elif download_type == "mp4":
            download_media(url, "mp4", lambda media: media.streams.get_highest_resolution(), "Downloaded")

    finally:
        download_in_progress = False
        download_button.config(state=tk.NORMAL, text="Download")


# Function to handle download button click
def on_download_button_click():
    url = url_entry.get()
    download_type = download_type_var.get()

    if url:
        threading.Thread(target=download_button_click_async, args=(url, download_type)).start()


# Create the main GUI window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x400")
root.configure(bg="#292929")

# Set up the style for GUI elements
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), background="#292929", foreground="white")
style.configure("TButton", font=("Helvetica", 12), background="#555555", foreground="#4B0082")
style.configure("TEntry", font=("Helvetica", 12), background="white", foreground="#4B0082")

# Create and place GUI elements
url_label = ttk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=(15, 0))

url_entry = ttk.Entry(root, width=40)
url_entry.pack()

# Create a radio button for selecting download type
download_type_var = tk.StringVar(value="mp3")
download_type_frame = ttk.Frame(root)
download_type_frame.pack(pady=(10, 0))

download_type_label = ttk.Label(download_type_frame, text="Choose Download Type:")
download_type_label.grid(row=0, column=0, padx=5)

mp3_radio_button = ttk.Radiobutton(download_type_frame, text="MP3", variable=download_type_var, value="mp3")
mp3_radio_button.grid(row=0, column=1, padx=5)

mp4_radio_button = ttk.Radiobutton(download_type_frame, text="MP4", variable=download_type_var, value="mp4")
mp4_radio_button.grid(row=0, column=2, padx=5)

download_button = ttk.Button(root, text="Download", command=on_download_button_click)
download_button.pack(pady=(10, 0))

# Create the Clear button to clear the URL entry
clear_button = ttk.Button(root, text="Clear", command=clear_url_field)
clear_button.pack(pady=(10, 0))

# Initialize the download_in_progress flag
download_in_progress = False

# Define download type labels
download_type_labels = {"mp3": "Downloaded mp3 files will be saved in:",
                        "mp4": "Downloaded mp4 files will be saved in:"}

# Create and display the destination folder labels
for download_type, label_text in download_type_labels.items():
    destination_label_text = f"{label_text} {MP3_PATH}" if download_type == "mp3" else f"{label_text} {MP4_PATH}"
    destination_label = ttk.Label(root, text=destination_label_text)
    destination_label.pack(pady=(15, 0))

    # Create the "Show" button to open the file location
    show_button = ttk.Button(root, text=f"Show {download_type} download Folder",
                             command=lambda dt=download_type: open_file_location(
                                 os.path.expanduser(MP3_PATH if dt == "mp3" else MP4_PATH)))
    show_button.pack(pady=(10, 0))

# Start the GUI event loop
root.mainloop()