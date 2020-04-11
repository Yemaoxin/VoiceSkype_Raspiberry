from snowboy import snowboydecoder
import sys
import signal
import playsound



interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def wakeup():
    playsound("../SystemSpeech/do.mp3")



model = "ye11.pmdl"

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=wakeup,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
