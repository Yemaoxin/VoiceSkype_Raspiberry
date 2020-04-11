# 受限于Mac的权限机制
# 先使用终端，rec  t.wav录取一段语音，获取到权限
# 然后在终端中执行python文件，曲线获得
import pyaudio
from  pyaudio import paInt16
import wave
framerate = 16000  # 采样率
num_samples = 1024  # 多少采样点为一个块
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = 'speech.wav'
record_second=5  #默认采样5秒，5秒内说话算数

def record():
    """
    录音函数，默认十五秒录音时间，暂时先这样
    :return: 写入speech.wav中的语音
    """
    audio=pyaudio.PyAudio()
    stream=audio.open(
        format=paInt16,channels=channels,rate=framerate,input=True,frames_per_buffer=num_samples    )
    frames=[]
    print("开始录音")
    stream.start_stream()
    for i in range(framerate//num_samples*record_second):
        data=stream.read(num_samples)
        frames.append(data)
    print("结束录音")
    stream.stop_stream()
    audio.terminate()
    with wave.open(FILEPATH,"wb") as f:
        f.setframerate(framerate)
        f.setnchannels(channels)
        f.setsampwidth(audio.get_sample_size(paInt16))
        f.writeframes(b''.join(frames))
if __name__ =="__main__":
    record()