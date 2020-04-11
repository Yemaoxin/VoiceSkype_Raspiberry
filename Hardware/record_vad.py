"""
  实现了实时的语音录入停止：VAD
  只有在有声音的才会录制
"""

import pyaudio
from pyaudio import paInt16
import webrtcvad
import wave
import  Hardware.wav2pcm  as wav2pcm
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
    vad = webrtcvad.Vad()
    vad.set_mode(0)
    frame = []
    framesNum=16000*20//1000
    stream = audio.open(format=paInt16, channels=channels, rate=framerate, input=True, frames_per_buffer=framesNum)

    stream.start_stream()
    print("开始录音")
    count=0
    speechnum=0
    while not (speechnum>speechCount and count>=10):
        data=stream.read(framesNum)
        frame.append(data)
        isSpeech=vad.is_speech(data,framerate)
        if(isSpeech):
            count=0
            speechnum+=1
        else:
            count+=1
        print("current speech:{}".format(isSpeech))
    stream.stop_stream()
    audio.terminate()
    with wave.open(filePath,"wb") as  f:
        f.setframerate(framerate)
        f.setnchannels(channels)
        f.setsampwidth(audio.get_sample_size(paInt16))
        f.writeframes(b"".join(frame))
    print("结束录音")
    pcm_path=filePath.split("wav")[0]+"pcm"   #生成pcm文件名
    wav2pcm.wav2pcm(filePath,pcm_path)

if __name__=="__main__":
    record_vad()
