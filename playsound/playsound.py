import os
def playsound(path):
    base_command="mplayer "
    base_command+=path
    os.system(base_command)

if __name__ =="__main__":
    playsound('../Music/test.mp3')