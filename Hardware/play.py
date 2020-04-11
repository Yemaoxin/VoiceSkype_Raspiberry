import wave
import pyaudio
from playsound import playsound
def play_wav(filepath):
    audio=pyaudio.PyAudio()
    chunk=1024
    with wave.open(filepath,'rb') as f:
        stream=audio.open(format=audio.get_format_from_width(f.getsampwidth()),rate=f.getframerate(),channels=f.getnchannels(),output=True)
        print("开始播放")
        data=f.readframes(chunk)
        while data!="" :  #非空播放
            stream.write(data)
            data = f.readframes(chunk)
        print('结束播放')
    stream.stop_stream()
    audio.terminate()
def play_mp3(path):
    playsound(path)
if __name__=="__main__":
    play_mp3("auido.mp3")

