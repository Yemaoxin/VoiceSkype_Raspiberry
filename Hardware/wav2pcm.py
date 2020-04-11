import os

def wav2pcm(wav_file="speech.wav",pcm_file="speech.pcm"):
    """
    调用ffmpeg转化，速度不快，但是并没有要求很快，数据上传可以慢一点
    只要不影响体验的话，不行就换回wav，wav的话估计没有很慢
    5秒以内的wav很快
    :param wav_file:
    :param pcm_file:
    :return:
    """
    os.system("ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s"%(wav_file,pcm_file))