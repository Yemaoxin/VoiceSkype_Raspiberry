import requests
import playsound
import vlc
import multiprocessing

class Player():

    # 作为类变量来说的话，共享似乎不是问题
    media = vlc.MediaPlayer()  # vlc功能太多太全了，MediaPlayer()不支持共享
    def __init__(self,):
        self.information="subProcess"
    def set_uri(self,uri):
         self.media.set_mrl(uri)

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

def searchNetMusic(name):
    base_url="http://45.40.201.185:3000/search?keywords="
    url=base_url+name
    try:
       result=requests.get(url).json()['result']['songs'][0]
       id=result['id']
       print(id)
       mp3_url="http://45.40.201.185:3000/song/url?br=320000&id="+str(id)
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
                player.play()
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
        play.value = 1
        import time

        time.sleep(10)
        play.value = 3









