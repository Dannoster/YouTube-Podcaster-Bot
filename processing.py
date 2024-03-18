from pytube import YouTube
# from pytube.innertube import _default_clients
# _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID"]
import requests
from moviepy.editor import AudioFileClip
import os

STORE_FOLDER = "materials"

def getting_lenth(url: str):
    video = YouTube(url)
    return video.length

def getting_audio(url: str):

    video = YouTube(url)
    # audio = video.streams.filter(only_audio=True, abr="50kbps").first()
    audio = video.streams.get_audio_only()
    title = video.title.strip()
    channel = video.author.strip()
    thumbnail = requests.get(video.thumbnail_url).content
    with open(f'{STORE_FOLDER}/out.jpg', 'wb') as handler:
        handler.write(thumbnail)
    audio_path = audio.download(f"{STORE_FOLDER}", f"out.mp4")

    mp4_size = os.stat(f"{STORE_FOLDER}/out.mp4").st_size/2**20 # in MB
    if mp4_size <= 49:
        os.rename(f"{STORE_FOLDER}/out.mp4", f"{STORE_FOLDER}/out.mp3")
    else:
        lenth = video.length
        max_bitr = 160
        max_relative_weight = 7200 * 55 #2 hours with 55k bitrate ~48MB
        if lenth * max_bitr <= max_relative_weight:
            bitr = max_bitr
        else:
            bitr = max_relative_weight // lenth
        video = AudioFileClip(f"{STORE_FOLDER}/out.mp4")
        video.write_audiofile(f"{STORE_FOLDER}/out.mp3", bitrate=f"{bitr}k", 
                            write_logfile=False, verbose=False, logger=None)
        os.remove(f"{STORE_FOLDER}/out.mp4")

    return title, channel

def clean(title):
    os.remove(f"{STORE_FOLDER}/out.mp3")
    os.remove(f"{STORE_FOLDER}/out.jpg")
    pass


# import eyed3
# audiofile = eyed3.load(f"{STORE_FOLDER}/out.mp3")
# audiofile.initTag()
# audiofile.tag.title = title
# audiofile.tag.artist = channel
# audiofile.tag.images.set(3, open(f'{STORE_FOLDER}/out.jpg','rb').read(), "imege/jpeg", u'Cover',)
# audiofile.tag.save(version=(2,3,0))