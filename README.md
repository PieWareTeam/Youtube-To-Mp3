# Youtube-To-Mp3
A simple Youtube to mp3 and mp4 converter/downloader

This Python application provides a graphical user interface (GUI) for downloading YouTube videos (MP4 format) or converting them to MP3 format. It offers a user-friendly way to save your favorite videos for offline watching/listening.
Enter a valid youtube url into the textfield, choose your file type (mp3 or mp4) and click download.
You can quickly access your downloaded audio or video files using the "Show download Folder" buttons.


## Features
- Choose between downloading the video in MP4 format or converting it to MP3.
- Automatically organizes downloaded files into 'mp3' and 'mp4' folders under a 'yt_downloads' directory on your desktop.
- Swiftly access your downloaded audio and video files via the "Show download Folder" buttons.
- Provides a simple and intuitive user interface using the Tkinter library.
- Supports threading to ensure a smooth and responsive user experience.

## How to Use

1. Enter a valid YouTube URL in the input field.
2. Choose whether you want to download the video in MP4 format or convert it to MP3.
3. Click the "Download" button to initiate the process. The application will show you the progress and notify you when the download is complete.
4. You can also click the "Clear" button to remove the entered URL from the input field.


# Download and use the prebuilt app
The official prebuilt windows app made from the code in main.py can be downloaded [here](https://github.com/PieWareTeam/Youtube-To-Mp3/releases).
Download the YoutubeToMp3.zip file.
The app has been build using pyinstaller which is why it can be incorrectly seen as malware by Windows.
[More info](https://medium.com/@markhank/how-to-stop-your-python-programs-being-seen-as-malware-bfd7eb407a7#:~:text=Code%20compiled%20using%20pyinstaller%20or,ml.)

# Or run the code on your machine
Download and run the code from your IDE or commandline.

## Getting Started

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the program by executing `python main.py`.

## Requirements

- Python 3.x
- The `pytube` library for downloading YouTube videos.
- Tkinter for the graphical user interface.


## Known bug and how to fix it
When the program keeps failing to download something it is likely due to pytube.exceptions.RegexMatchError.
The fix -> open your IDE -> go to /venv/lib/site-packages/pytube -> change line 30 in cipher.py from ```var_regex = re.compile(r"^\w+\W")``` to ```var_regex = re.compile(r"^\$*\w+\W") ```

## Disclaimer

This program is intended for personal and educational purposes only. Please respect copyright laws and YouTube's terms of service when using this tool.
