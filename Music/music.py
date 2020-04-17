import requests
import sys
sys.path.append("..")
from playsound import playsound
import vlc
import multiprocessing
class Player():
    # vlc本身是一个异步的进程，不需要另外开一个进程
    media = vlc.MediaPlayer()  # vlc功能太多太全了，MediaPlayer()不支持共享
    def __init__(self,):
        self.information="subProcess"
        self.playing_uri=''
    def set_uri(self,uri):
         self.media.set_mrl(uri)
         self.playing_uri=uri

    def play(self,path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else :
            self.media.play()

    # 暂停播放
    def pause(self):
        self.media.pause()

    # 恢复播放
    def resume(self):
        self.media.set_pause(0)

    #  停止播放
    def stop(self):
        self.media.stop()
        self.media.release()
        self.playing_uri=""      # 只要没有释放，就可以知道

    # 释放资源
    def release(self):
        return self.media.release()

    # 是否正在播放
    def is_playing(self):
            return self.media.is_playing()

    def add_volume(self):
        # 一次增加5个音量值
        volume=self.media.audio_get_volume()
        self.media.audio_set_vloume(volume+5)

    def sub_volume(self):
        # 一次减少5个音量值
        volume=self.media.audio_get_volume()
        self.media.audio_set_volume(volume-5)

    def is_end(self):
        return (1.0-self.media.get_position())<=0.001
# class Player():
#
#     # 作为类变量来说的话，共享似乎不是问题
#     # vlc功能太多太全了，MediaPlayer()不支持共享
#
#     def __init__(self,):
#         self.information="subProcess"
#     def set_uri(self,uri):
#         self.media = OMXPlayer(uri)
#         self.media.set_volume(0.3)
#
#     def play(self,path=None):
#         if path:
#             self.set_uri(path)
#
#     # 暂停播放
#     def pause(self):
#         self.media.pause()
#
#     # 恢复播放
#     def resume(self):
#         self.media.play_pause()
#
#     #  停止播放
#     def stop(self):
#         self.media.stop()
#
#
#     # 是否正在播放
#     def is_playing(self):
#             return self.media.is_playing()
#
#     def add_volume(self):
#         # 一次增加5个音量值
#         volume=self.media.volume()
#         self.media.set_vloume(volume+0.1)
#
#     def sub_volume(self):
#         # 一次减少5个音量值
#         volume=self.media.volume()
#         self.media.set_volume(volume-0.1)
#
#     def is_end(self):
#         return (1.0-self.media.get_time_position()/self.media.get_time_length())<=0.001

def searchNetMusic(name):
    base_url="http://localhost:3000/search?keywords="
    url=base_url+name
    import logging
    logging.warning(url)
    try:
       result=requests.get(url).json()['result']['songs'][0]
       id=result['id']
       print(id)
       mp3_url="http://localhost:3000/song/url?br=320000&id="+str(id)
       url_result=requests.get(mp3_url).json()['data'][0]['url']
       print(url_result)
       return url_result
    except Exception as e:
        print("Error")

def run(play,uri):
    """
    多进程函数，重点：play和uri必须是共享内存
    :param play: 共享内存，控制信号
    :param uri: Manager共享，uri信息 ,list
    :return:
    """
    player=Player()
    while True:
        if   play.value < 1:  # 当播放标志位未设置时，一直卡住
            continue
        elif play.value>=1:          # 正在播放
            if (play.value==1):      # 1代表播放，但没设置uri
                player.set_uri(uri[0])
                play.value=2         # 2代表播放中,无需处理
            elif play.value==3:      # 3暂停命令已经发出，但没暂停
                player.pause()
                play.value=4         # 4已经暂停
            elif play.value==5:      # 5回复命令已经发出但未恢复
                play.value=2         # 2的时候才会播放
                player.resume()
            elif play.value==7:      # 停止播放的命令发出
                play.value=0
                player.stop()
            elif play.value==8:      # 8增加音量
                player.add_volume()
                play.value=2
            elif play.value==9:      # 9降低音量
                player.sub_volume()
                play.value=2




if __name__=="__main__":
    # Q=Queue(10)
    # 通过更新的多进程共享的思路实现了
    with multiprocessing.Manager() as manager:
        play = multiprocessing.Value('i', 0)
        uri = manager.list()
        uri.append("0")
        process = multiprocessing.Process(target=run, args=(play, uri,))
        process.start()
        uri[0] = searchNetMusic("麻雀")
        print(searchNetMusic("麻雀"))
        play.value = 1
        import time
        print("播放音乐")
        time.sleep(100)
        play.value = 3
    # player=Player()
    # player.set_uri("http://m7.music.126.net/20200417085116/affe4300c88a00dc40537fbdfa9dc0e7/ymusic/555b/0f58/0609/b1e0b087cb826dde13b21cbaa504f963.mp3")
    # player.play()
    # import time
    # time.sleep(10)
    # player.stop()










