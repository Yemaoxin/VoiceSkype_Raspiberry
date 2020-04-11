import  pathlib
import sys
sys.path.append("..")
import Wakeup.wake as wake
from snowboy import snowboydecoder
import signal
import playsound
import  Hardware.record_vad as record_vad
import Speech.SpeechRecognition as SpeechRecognition
from Speech.SpeechRecognition import SmallChat_callback

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

if __name__ =="__main__":

    interrupted = False

    model = "../ye11.pmdl"

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)


    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.464)
    print('Listening... Press Ctrl+C to exit')
    # main loop
    detector.start(detected_callback=wakeup,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)
    detector.terminate()




