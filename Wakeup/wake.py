"""
    部分已经弃用
"""
import sys
sys.path.append("..")
from snowboy import snowboydecoder
from snowboy import snowboydetect

API_TOKEN="0a5fad2d4d0a810864dabb11b6000699bb5ce797"
import Hardware.record_vad as record
from playsound import playsound
import sys
import base64
import requests
import chardet
from snowboy import snowboydecoder
import signal
from  Speech  import SpeechRecognition


def get_wave(fname):
        with open(fname, "rb") as infile:
            p = base64.b64encode(infile.read())
            print(str(p, "utf-8"))
            return str(p, "utf-8")

endpoint = "https://snowboy.kitt.ai/api/v1/train/"
token = API_TOKEN
hotword_name = "叶恬恬"
language = "zh"
age_group = "20_29"
gender = "M"
microphone = "usb microphone"
def trainHotWord(wav1,wav2,wav3,out):
    """
    通过snowboy训练自己的声音模型
    :param wav1: 语音1
    :param wav2: 语音2
    :param wav3: 语音3
    :param out:  模型输出文件 pmdl格式
    :return:
    """
    data = {
        "name": hotword_name,
        "language": language,
        "age_group": age_group,
        "gender": gender,
        "microphone": microphone,
        "token": token,
        "voice_samples": [
            {"wave": get_wave(wav1)},
            {"wave": get_wave(wav2)},
            {"wave": get_wave(wav3)}
        ]
    }
    response = requests.post(endpoint, json=data)
    if response.ok:
        with open(out, "wb") as outfile:
            outfile.write(response.content)
        print ("Saved model to '%s'." % out)
    else:
        print ("Request failed.")
        print ( response.text)


def signal_handler(signal, frame):
        global interrupted
        interrupted = True


def interrupt_callback():
        global interrupted
        return interrupted


def wakeup():
        playsound.playsound("../SystemSpeech/do.mp3")
        record.record_vad("Command.wav")
        SpeechRecognition()

def recordAndtrain():
    playsound.playsound("../SystemSpeech/trainVoice/start_set.mp3")
    playsound.playsound("../SystemSpeech/trainVoice/start_set1.mp3")
    record.record_vad("wav1.wav")
    playsound.playsound("../SystemSpeech/trainVoice/start_set2.mp3")
    record.record_vad("wav2.wav")
    playsound.playsound("../SystemSpeech/trainVoice/start_set3.mp3")
    record.record_vad("wav3.wav")
    playsound.playsound("../SystemSpeech/trainVoice/training.mp3")
    trainHotWord(wav1="wav1.wav",wav2="wav2.wav",wav3="wav3.wav",out="ye11.pmdl")


