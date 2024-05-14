import os
import unicodedata
from pytube import YouTube, exceptions
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from colorama import Fore, Style
from tqdm import tqdm

class YouTubeDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Video Downloader")
        self.geometry("500x400")

        # Create a style object
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))

        # Add YouTube logo
        logo_path = "youtube_logo.png"
        logo_image = Image.open(logo_path)
        logo_photo = ImageTk.PhotoImage(logo_image.resize((100, 60), Image.LANCZOS))
        logo_label = tk.Label(self, image=logo_photo)
        logo_label.image = logo_photo
        logo_label.pack(pady=10)

        # URL input
        url_label = tk.Label(self, text="Enter YouTube Video URL:", font=("Arial", 14))
        url_label.pack(pady=5)
        self.url_input = ttk.Entry(self, width=50, font=("Arial", 12))
        self.url_input.pack(pady=5)

        # Download button
        download_button = ttk.Button(self, text="Download", command=self.download_video, width=15, style="TButton")
        download_button.pack(pady=10)

        # Resolution dropdown
        self.resolution_var = tk.StringVar()
        resolution_label = tk.Label(self, text="Select Resolution:", font=("Arial", 12))
        resolution_label.pack(pady=5)
        self.resolution_dropdown = ttk.Combobox(self, textvariable=self.resolution_var, state="readonly", font=("Arial", 12))
        self.resolution_dropdown.pack(pady=5)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self, mode="determinate", length=400)
        self.progress_bar.pack(pady=10)

        # Download status label
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def download_video(self):
        url = self.url_input.get()
        try:
            yt = YouTube(url)
            available_streams = yt.streams.filter(progressive=True).order_by("resolution")
            resolutions = [stream.resolution for stream in available_streams]
            self.resolution_dropdown["values"] = resolutions
            self.resolution_dropdown.bind("<<ComboboxSelected>>", lambda event: self.start_download(yt))
        except exceptions.AgeRestrictedError:
            print(f"{Fore.RED}This video is age-restricted and cannot be downloaded.")
        except Exception as e:
            print(f"{Fore.RED}YouTube Video Download Failed: {e}")

    def start_download(self, yt):
        resolution = self.resolution_var.get()
        available_streams = yt.streams.filter(progressive=True).order_by("resolution")
        stream = next(filter(lambda s: s.resolution == resolution, available_streams), None)
        if stream:
            self.download_progress = 0
            self.progress_bar.start()
            stream.download(output_path="youtube_video", filename=self.sanitize_title(yt.title) + ".mp4")
            self.status_label.config(text="Download Successful!", fg="green")
            self.progress_bar.stop()
        else:
            self.status_label.config(text="Selected resolution not available.", fg="red")

    def sanitize_title(self, title):
        return "".join(c for c in title if c.isalnum() or c in " -_")

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()