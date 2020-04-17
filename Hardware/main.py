from aip import AipSpeech
APP_ID="18754384"
APP_KEY="VjxtYrtYNaN7RIchnj0MfE7H"
SECRET_KEY="VyXqlikq1LNnDd2cQ9sfwQO2ghGFenWZ"
skype_name="1648428830@qq.com"
skype_password="123456789ymx"


import pyaudio
from pyaudio import paInt16
import webrtcvad
import wave
import  wav2pcm
framerate = 16000
channels = 1
FILEPATH="speech.wav"
samplewidth=2
frame_duration=20  #二十毫秒的设置

def record_vad(filePath="speech.wav",speechCount=40):
    """
    测试时发现鸟叫声也会造成影响，可以设定连续200-300ms的时间
    :return:
    """
    audio = pyaudio.PyAudio()
    wf=wave.open('speech.wav')
    vad = webrtcvad.Vad()
    vad.set_mode(0)
    frame = []
    framesNum=16000*20//1000
    stream=audio.open(format=p.get_format_from_width(wf.getsampwidth()),
           channels=wf.getnchannels(),
           rate=wf.getframerate(),
           output=True)
    while True:
        data = wf.readframes(1000)  # 从音频流中读取1000个采样数据，data类型为str.注意对音频流的读写都是字符串
        if data == "":  # 判断是否结束
            break
        isSpeech=vad.is_speech(data,framerate)
        print(isSpeech)
         # 从wf中读数据，然后写到stream中。就是从文件中读取数据然后写到声卡里
    stream.stop_stream()
    audio.terminate()

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
def test_webrtc():
    audio = pyaudio.PyAudio()
    wf = wave.open('speech.wav')
    vad = webrtcvad.Vad()
    vad.set_mode(0)
    frame = []
    framesNum = 16000 * 20 // 1000
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    while True:
        data = wf.readframes(framesNum)  # 从音频流中读取1000个采样数据，data类型为str.注意对音频流的读写都是字符串
        if data == "":  # 判断是否结束
            break
        isSpeech = vad.is_speech(data, framerate)
        print(isSpeech)
        # 从wf中读数据，然后写到stream中。就是从文件中读取数据然后写到声卡里
    stream.stop_stream()
    audio.terminate()


if __name__=="__main__":
     test_webrtc()