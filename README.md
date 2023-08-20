# Youtube-To-Mp[3,4]
A simple Youtube to mp3 and mp4 converter/downloader

This Python application provides a graphical user interface (GUI) for downloading YouTube videos (MP4 format) or converting them to MP3 format. It offers a user-friendly way to save your favorite videos for offline watching/listening.
Enter a valid youtube url into the textfield, choose your file type (mp3 or mp4) and click download.
You can quickly access your downloaded audio or video files using the "Show download Folder" buttons.


## Features
- Choose between downloading the video in MP4 format or converting it to MP3.
- Automatically download entire playlists
- Automatically organizes downloaded files into 'mp3' and 'mp4' folders under a 'yt_downloads' directory on your desktop.
- Swiftly access your downloaded audio and video files via the "Show download Folder" buttons.
- Provides a basic and intuitive user interface using the Tkinter library.
- Supports threading to ensure a smooth and responsive user experience.

# How to Use

## Single video
1. Enter a valid YouTube URL in the input field.
2. Choose whether you want to download the video in MP4 format or convert it to MP3.
3. Click the "Download" button to initiate the process. The application will notify you when the download is complete.

## Entire playlist
1. Enter a valid YouTube playlist URL in the input field.
2. Choose whether you want to download the videos in MP4 format or convert it to MP3.
3. Make sure the "Playlist" checkbox is checked
4. Click the "Download" button to initiate the process. The application will notify you when the download is complete.
5. The amount of files that still have to be downloaded will be displayed and updated automatically
6. side info: The playlist has to be public on Youtube for the program to access and download it



# Download and use the prebuilt app
The official prebuilt windows app made from the code in main.py can be downloaded [here](https://github.com/PieWareTeam/Youtube-To-Mp3/releases/tag/v01.8).
Download the setup file, run it and follow the steps.
All of the code is open source and can be viewed [here](https://github.com/PieWareTeam/Youtube-To-Mp3/blob/master/main.py)

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
Try to find the cipher.py file and moddify line 30 from ```var_regex = re.compile(r"^\w+\W")``` to ```var_regex = re.compile(r"^\$*\w+\W") ```.
Example:
Open your IDE -> go to /venv/lib/site-packages/pytube -> change line 30 in cipher.py.


## Build the application
When you are done making changes to the code or adding some code, you can run [this](https://github.com/PieWareTeam/Youtube-To-Mp3/blob/master/pyinstallerCommand.txt) command in the root directory of the project
to build the .exe file. Keep in mind that you might have to moddify the command depending on the changes you made to the project.

## Disclaimer

This program is intended for personal and educational purposes only. Please respect copyright laws and YouTube's terms of service when using this tool.
