import os
import sys
import tkinter as tk
import subprocess
import threading
from tkinter import messagebox, ttk
from pytube import YouTube, Playlist
from datetime import datetime
import queue

class YoutubeToMpConverter:
    def __init__(self):
        self.setup_paths()
        self.setup_gui()

    def setup_paths(self):
        self.DESKTOP_PATH = os.path.expanduser("~/Desktop")
        self.YT_DOWNLOADS_PATH = os.path.join(self.DESKTOP_PATH, "yt_downloads")
        self.MP3_PATH = os.path.join(self.YT_DOWNLOADS_PATH, "mp3")
        self.MP4_PATH = os.path.join(self.YT_DOWNLOADS_PATH, "mp4")

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("YouTube To Mp[3,4]")
        self.root.geometry("730x550")
        self.root.minsize(730, 550)
        self.root.configure(bg="#292929")

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 12, "bold"), background="#292929", foreground="#84C9Fb")
        self.style.configure("TButton", font=("Helvetica", 12), background="#000000", foreground="#000000", borderwidth=0, focuscolor="#292929")
        self.style.map("TButton", background=[("active", "#84C9Fb"), ("disabled", "#555555")], foreground=[("active", "#292929")])
        self.style.configure("TEntry", font=("Helvetica", 12), background="white", foreground="#000000")

        self.url_label = ttk.Label(self.root, text="Enter YouTube URL:")
        self.url_label.pack(pady=(15, 0))

        self.input_frame = ttk.Frame(master=self.root)
        self.url_entry = ttk.Entry(master=self.input_frame, width=40)
        self.download_type_var = tk.StringVar(value="mp3")
        self.mp3_radio_button = ttk.Radiobutton(self.input_frame, text="MP3", variable=self.download_type_var, value="mp3")
        self.mp4_radio_button = ttk.Radiobutton(self.input_frame, text="MP4", variable=self.download_type_var, value="mp4")

        self.url_entry.pack(side='left')
        self.mp3_radio_button.pack(side='left')
        self.mp4_radio_button.pack()
        self.input_frame.pack(pady=5)

        self.playlist_checkbox_var = tk.IntVar()
        self.playlist_checkbox = tk.Checkbutton(self.root, text="Playlist", variable=self.playlist_checkbox_var)
        self.playlist_checkbox.pack(pady=5)

        self.download_button = ttk.Button(self.root, text="Download", command=self.on_download_button_click)
        self.download_button.pack(pady=(10, 0))

        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_url_field)
        self.clear_button.pack(pady=(10, 0))

        self.download_status_label = ttk.Label(self.root, text="", font=("Helvetica", 10))
        self.download_status_label.pack(pady=(10, 50))

        self.download_type_labels = {"mp3": "Downloaded mp3 files will be saved in:", "mp4": "Downloaded mp4 files will be saved in:"}

        for download_type, label_text in self.download_type_labels.items():
            destination_label_text = f"{label_text} {self.MP3_PATH}" if download_type == "mp3" else f"{label_text} {self.MP4_PATH}"
            destination_label = ttk.Label(self.root, text=destination_label_text)
            destination_label.pack(pady=(10, 0))

            show_button = ttk.Button(self.root, text=f"Show {download_type} download Folder", command=lambda dt=download_type: self.open_file_location(os.path.expanduser(self.MP3_PATH if dt == "mp3" else self.MP4_PATH)))
            show_button.pack(pady=(10, 25))

        self.playlist_queue = queue.Queue()
        self.download_in_progress = False

    def throw_popup(self, title, message, error=True):
        messagebox.showerror(title, message) if error else messagebox.showinfo(title, message)

    def clear_url_field(self):
        self.url_entry.delete(0, tk.END)

    def open_file_location(self, download_folder):
        try:
            if sys.platform.startswith('win'):
                subprocess.Popen(['explorer', os.path.normpath(download_folder)])
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', download_folder])
            elif sys.platform.startswith('linux'):
                subprocess.Popen(['xdg-open', download_folder])
            else:
                self.throw_popup("Error", "Unsupported platform for opening file location.")
        except Exception:
            self.throw_popup("Error", "Directory doesn't exist yet but will be created automatically after you download something")

    def download_media(self, url, media_type, format_function, success_message):
        try:
            media = YouTube(url)
            stream = format_function(media)
            if stream:
                download_folder = self.MP3_PATH if media_type == "mp3" else self.MP4_PATH
                if self.playlist_checkbox_var.get():
                    download_folder = os.path.join(download_folder, self.PLAYLIST_PATH)
                if not os.path.exists(download_folder):
                    os.makedirs(download_folder)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_file_name = f"{media.title}_{timestamp}.{media_type}"
                print(f"Downloading {media_type}: {media.title}")
                stream.download(output_path=download_folder, filename=new_file_name)
                if not self.playlist_checkbox_var.get():
                    self.throw_popup("Completed successfully", f"{success_message}: {new_file_name}", False)
            else:
                self.throw_popup("Error", f"No {media_type} stream found for the provided URL")
        except Exception as e:
            if not self.playlist_checkbox_var.get():
                self.throw_popup("Error", e)

    def enable_interaction(self):
        self.download_button.config(state=tk.NORMAL, text="Download")
        self.mp4_radio_button.config(state=tk.NORMAL)
        self.mp3_radio_button.config(state=tk.NORMAL)
        self.playlist_checkbox.config(state="normal")
        self.download_status_label.config(text="Download completed")

    def disable_interaction(self):
        self.download_button.config(state=tk.DISABLED, text="Downloading...")
        self.playlist_checkbox.config(state="disabled")
        self.mp4_radio_button.config(state=tk.DISABLED)
        self.mp3_radio_button.config(state=tk.DISABLED)

    def download_button_click_async(self, url, download_type):
        if self.download_in_progress:
            return
        try:
            self.download_in_progress = True
            self.disable_interaction()

            if download_type == "mp3":
                self.download_media(url, "mp3", lambda media: media.streams.filter(only_audio=True).first(),
                                    "Downloaded and converted")
            elif download_type == "mp4":
                self.download_media(url, "mp4", lambda media: media.streams.get_highest_resolution(), "Downloaded")

        except Exception as e:
            self.throw_popup("Error", f"An error occurred: {e}")
        finally:
            self.download_in_progress = False
            self.enable_interaction()
            self.download_status_label.config(text="Download completed")

    def download_playlist(self, url):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            playlist = Playlist(url)
            self.PLAYLIST_PATH = f"{playlist.title}_{timestamp}"
            for video in playlist.videos:
                self.playlist_queue.put(video.watch_url)

        except Exception:
            self.throw_popup("Error", "Invalid YouTube playlist URL")

    def download_playlist_worker(self, media_type):
        try:
            while not self.playlist_queue.empty():
                video_url = self.playlist_queue.get()
                self.download_button_click_async(video_url, media_type)
                self.playlist_queue.task_done()
                self.download_status_label.config(text=f"Downloading: {self.playlist_queue.qsize()} files remaining")
        except Exception as e:
            self.throw_popup("Error", f"An error occurred while downloading playlist: {e}")
        finally:
            self.throw_popup("Playlist", "Downloaded", False)
            self.download_status_label.config(text="Download completed")

    def on_download_button_click(self):
        url = self.url_entry.get()
        self.download_status_label.config(text="")
        if url:
            download_type = self.download_type_var.get()
            try:
                if self.playlist_checkbox_var.get():
                    self.download_playlist(url)
                    threading.Thread(target=self.download_playlist_worker, args=(download_type,)).start()
                else:
                    threading.Thread(target=self.download_button_click_async, args=(url, download_type)).start()
            except Exception as e:
                self.throw_popup("Error", f"An error occurred: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    converter = YoutubeToMpConverter()
    converter.run()
