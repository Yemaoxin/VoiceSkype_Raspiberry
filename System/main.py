import  pathlib
import sys
sys.path.append("..")
import Wakeup.wake as wake
from snowboy import snowboydecoder
import signal
from playsound import playsound
import  Hardware.record_vad as record_vad
import Speech.SpeechRecognition as SpeechRecognition
from Speech.SpeechRecognition import SmallChat_callback
import os


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def wakeup():
    """
    弃用
    :return:
    """
    playsound.playsound("../SystemSpeech/service/do.mp3")
    command_path="command.wav"
    record_vad.record_vad(filePath=command_path,speechCount=50)  #当前文件夹   命令时长应比较长
    command_path=command_path.split('wav')[0]+"pcm"
    SpeechRecognition.Recognition(command_path)     #识别并做处理


if  __name__ =="__main__":
   path=pathlib.Path("ye11.pmdl")
   if(not path.exists()):
       wake.recordAndtrain()

   interrupted = False

   model = "ye11.pmdl"

   # capture SIGINT signal, e.g., Ctrl+C
   signal.signal(signal.SIGINT, signal_handler)

   #可以将队列数据放在这里
   smallchat=SmallChat_callback()
   detector = snowboydecoder.HotwordDetector(model, sensitivity=0.465)   #通过简单测试出来的敏感度，可以调整
   print('Listening... Press Ctrl+C to exit')
   # main loop
   detector.start(detected_callback=smallchat.wakeup,
                  interrupt_check=interrupt_callback,
                  sleep_time=0.03)
   detector.terminate()




