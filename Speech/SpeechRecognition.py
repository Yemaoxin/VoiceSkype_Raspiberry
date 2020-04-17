from aip import AipSpeech
import sys
sys.path.extend('..')
from weather import getWeather
from pampy import match,_
from Hardware  import  record_vad
import requests
import Speech.SpeechSynthesis as SpeechSynthesis
import re
from playsound import playsound
from Skype import getTime as getTime
from  snowboy import snowboydecoder
import signal
from Music import music
from Hardware import record_vad
from SmallChat import SmallChat
import multiprocessing
from Skype import SkpyeEvent
import ctypes
## api接口的参数，账号
APP_ID="18754384"
APP_KEY="VjxtYrtYNaN7RIchnj0MfE7H"
SECRET_KEY="VyXqlikq1LNnDd2cQ9sfwQO2ghGFenWZ"
skype_name="1648428830@qq.com"
skype_password="123456789ymx"

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

class  matchCode:
    def __init__(self):
        self.code=0             #  code 代表现在处理的问题的类型
        self.date=0             #  date 查询天气的日期
        self.location=''        #  location 查询天气的地址
        self.contract=''        #  contract 发送消息的联系人
        self.music=""           #  music 播放音乐的音乐名
    def setWeatherCode(self,num,location='',date=0):
        """
        天气设置
        主要是为了在match中返回信息到等号左边
        :param num:
        :param location:
        :param date:
        :return:
        """
        self.code=num
        self.location=location
        self.date=date
        return  self.date,self.location
    def getCode(self):
        return self.code

    def setTimeCode(self,code):
        """
        时间设置
        主要是为了在match中返回信息到等号左边
        :param code:
        :return:
        """
        self.code=code    #读取时间时间是code5
        return self.code

    def setChatCode(self,code=10,contract=""):
        """
        主要是为了返回联系人到等号左边。

        :param code:
        :param contract:
        :return:
        """
        self.code=code
        self.contract=contract
        return code,contract
    def setMusicCode(self,code=20,music_name=""):  # 20作为识别的代码
        # 主要是提供返回值，在规则匹配时作为match函数的返回值，返回匹配出来的信息
        self.music=music_name
        self.code=code
        return self.code,self.music

class SmallChat_callback:
    def __init__(self):
        """
        专门为闲聊设置的回调类，主要是为了数据能够传入回调函数
        """
        self.status=0                             # 0代表命令模式  1代表闲聊模式
        self.finished=False
        self.player=music.Player()                # 开启vlc
        self.OldVaule=0

        # # 设置skype时间循环，同时拿出friends列表
        # 设置skype时间循环，同时拿出friends列表
        self.SkpyeEvent = SkpyeEvent.SkypePing(skype_name, skype_password)
        # friends字典
        self.friends = self.SkpyeEvent.getFriends()
        # 开启Skype子进程
        self.subProcessing = multiprocessing.Process(target=SkpyeEvent.run, args=(self.SkpyeEvent,))
        self.subProcessing.daemon = True  # 设置子进程为父进程的守护进程（伴随进程），父进程死亡则子进程一起死亡
        self.subProcessing.start()

    def wakeup(self):
        """
        通过小瓜小瓜的唤醒词进入的状态有两种
        1、命令模式：要符合命令的格式才会有响应
        2、闲聊模式：随便聊

        如果过程中出现网络错误，将会被此处劫住，然后进行语音提示
        :return:None
        """
        try:
            self.controled=0
            self.oldValue=0
            if(self.player.is_playing()):
                # 如果还在播放音乐
                self.player.pause()     # 先暂停播放
                self.controled=1        # 记录：发生过暂停
                self.oldValue=3         # 记录：每次修改时纪录旧值，如果不等于3，代表后面使用的其他关键的控制
            playsound.playsound("../SystemSpeech/service/do.mp3")
            if self.status == 0:
                command_path = "command.wav"
                record_vad.record_vad(filePath=command_path, speechCount=50)  # 当前文件夹   命令时长应比较长
                command_path = command_path.split('wav')[0] + "pcm"
                self.Recognition(command_path)  # 识别并做处理
            else:
                # 闲聊的时长限制多一些
                self.smallchat()
            # 产生语音控制时，会停止播放音乐
            # 只有oldValue==3才会继续播放
            if( self.controled==1 and self.oldValue==3):
                # 当发生了暂停、终止等命令后，不会进入此处
                print('触发恢复')
                self.player.resume()
                self.controled=0
                self.oldValue=0
        except ConnectionError as  e:
            playsound.playsound("../SystemSpeech/service/netCheck.mp3")


    def break_check(self):
        """
        未使用，实际无使用
        :return:
        """
        return self.finished

    def smallchat(self):
        """
        进行闲聊，包含比较多的错误处理
        利用了百度语音识别和腾讯闲聊API
        :return:
        """
        try:
            code=record_vad.record_vad("smallchat.wav", 50)  # 产生一个smallchat.pcm文件在底层
            if(code==-2):
                return    #认定识别错误，结束
            speech = AipSpeech(APP_ID, APP_KEY, SECRET_KEY)
            p = speech.asr(get_file_content('smallchat.pcm'), 'pcm', 16000, {
                'dev_pid': 1537,
            })
            command = p['result'][0]     #从json中提取识别出来的文字
            print(command)
            if (command == ""):
                playsound.playsound("../SystemSpeech/service/sorry.mp3")
                print("无法明白")
                return
            elif (command == "退出闲聊模式。"):
                playsound.playsound("../SystemSpeech/service/end_chat.mp3")
                print("退出闲聊模式")
                self.status = 0
                return
            else:
                # 封装好的闲聊函数
                response = SmallChat.sendQuestion(command)
                if(response==None):
                    return
                print(response)
                SpeechSynthesis.Synthesis(response, "smallchatResponse.mp3")
                playsound.playsound("smallchatResponse.mp3")
        except Exception as  e:
            playsound.playsound("../SystemSpeech/service/netCheck.mp3")

    def sendMessage(self, message="", contract=""):
        """
        发送Skype消息
        :param message: 发送的消息
        :param contract: 联系人的display_name
        :return: None
        """
        friend = ""  # 因为通过语音识别得到的人民不一定包含姓,通过匹配得出朋友的display_name
        for i in self.friends.keys():
            if (contract in i or contract == i):
                friend = self.friends[i]
                break
        if (friend == ""):
            return -1
        else:
            # 发送消息
            try:
              friend.chat.sendMsg(message)
            except requests.ConnectionError as e:
                try:
                  friend.chat.sendMsg(message)
                except requests.ConnectionError as e:
                    return -1
            return 0


    def Recognition(self,Path='Hardware/speech.pcm'):
        """
        命令模式下的识别，编写的规则的主体
        通过正则表达式的匹配和match进行匹配，通过match的返回值进行处理
        :param Path:
        :return:
        """
        speech = AipSpeech(APP_ID, APP_KEY, SECRET_KEY)
        p = speech.asr(get_file_content(Path), 'pcm', 16000, {
            'dev_pid': 1537,
        })
        code = matchCode()
        # 一旦匹配就会立即返回不会再进行匹配
        if not p["err_no"]==0:     #发生错误时,提示网络问题同时返回
            playsound.playsound("../SystemSpeech/service/netCheck.mp3")
            return
        command = p['result'][0]
        print(command)
        if ("天气" in command):      #天气模块
            imformation = match(p['result'][0],
                                re.compile("^今天天气怎么样"), code.setWeatherCode(num=1),
                                re.compile("^明天天气怎么样"), code.setWeatherCode(num=2, date=1, location=""),
                                re.compile("^(\S+)今天天气怎么样"), lambda x: code.setWeatherCode(4, date=0, location=x),
                                re.compile("^(\S+)明天天气怎么样"), lambda x: code.setWeatherCode(8, date=1, location=x),
                                strict=False
                                )
            print(imformation)
            if (not imformation):
                playsound.playsound('../SystemSpeech/service/sorry.mp3')
                return
            information = getWeather.getWeather(date=imformation[0], city=imformation[1])
            SpeechSynthesis.Synthesis(information, "response.mp3")
            playsound.playsound("response.mp3")
        elif ("现在" in command):        #  时间匹配
            imformation = match(command,
                                re.compile("现在是几点钟"), code.setTimeCode(5),
                                re.compile("现在的时间是多少"), code.setTimeCode(6),
                                strict=False)
            if (not imformation):
                playsound.playsound("../SystemSpeech/service/sorry.mp3")
                return
            nowTime = ""
            if (imformation == 5):
                nowTime = getTime.getTime()
            elif imformation == 6:
                nowTime = getTime.getFullTime()
            SpeechSynthesis.Synthesis(nowTime, "response.mp3")
            playsound.playsound("response.mp3")
        elif ("进入闲聊模式" in  command):    # 闲聊只需要切换status变量即可
            print("进入闲聊模式")
            self.status=1
        elif ("几点钟" in command ):         #  时间，只是命令匹配不同关键字
            nowTime = ""
            nowTime = getTime.getFullTime()
            SpeechSynthesis.Synthesis(nowTime, "response.mp3")
            playsound.playsound("response.mp3")
        elif ("发送消息" in command):  # 设定从10 开始设定为发送消息的code
            imformation = match(command,
                                re.compile("^发送消息给(\S+)。"), lambda x: code.setChatCode(code=10, contract=x),
                                re.compile("^给(\S+)发送消息"), lambda x: code.setChatCode(code=10, contract=x),
                                re.compile("^给(\S+)发送一条消息"), lambda x: code.setChatCode(code=10, contract=x),
                                strict=False
                                )
            if not imformation:  # 上述匹配代码匹配的话，如果失败会返回false，false即没有匹配上任何规则
                playsound.playsound("../SystemSpeech/service/sorry.mp3")
                return
            else:
                if len(self.friends) == 0:  # 如果由于网络原因，还未获得联系人字典的话，重新获取
                    playsound.playsound('../SystemSpeech/service/retry.mp3')
                    self.friends = self.SkpyeEvent.getFriends()
                    if len(self.friends) == 0:
                        playsound.playsound("../SystemSpeech/service/netCheck.mp3")
                        return
                whatMesssage = "发什么消息给" + imformation[1]
                SpeechSynthesis.Synthesis(whatMesssage, "../SystemSpeech/service/whatMessage.mp3")  # 根据联系人实时生成语音提示
                playsound.playsound("../SystemSpeech/service/whatMessage.mp3")
                record_vad.record_vad("message_contents.mp3", speechCount=50)
                message2text = speech.asr(get_file_content("message_contents.mp3"), 'pcm', 16000, {
                    'dev_pid': 1537,
                })
            # 语音发送失败会返回-1
            if (self.sendMessage(message=message2text['result'][0],
                                 contract=imformation[1]) == -1):  # imfotmation[1]是朋友的名称
                # 发送的消息如果失败了
                playsound.playsound("../SystemSpeech/service/contractNotFound.mp3")
            else:
                playsound.playsound("../SystemSpeech/Skype/sendSuccess.mp3")

        elif "回复消息" in command:  # 发送Skype消息，不一样的匹配规则
            imformation, friend = match(command,
                                        re.compile("给(\S+)回复消息"), lambda x: code.setChatCode(10, x),
                                        re.compile("回复消息"), code.setChatCode(code=11))
            if (not imformation == 10):
                playsound.playsound("../SystemSpeech/Skype/chooseWho.mp3")
                record_vad.record_vad("../SystemSpeech/Skype/who.wav", 40)
                friend = speech.asr(get_file_content('../SystemSpeech/Skype/who.pcm'), 'pcm', 16000, {
                    'dev_pid': 1537,
                })['result'][0]

            playsound.playsound("../SystemSpeech/Skype/whatMessage.mp3")
            record_vad.record_vad("../SystemSpeech/Skype/whatMessage.wav", 40)
            message = speech.asr(get_file_content('../SystemSpeech/Skype/whatMessage.pcm'), 'pcm', 16000, {
                'dev_pid': 1537,
            })['result'][0]
            if (self.sendMessage(message=message, contract=friend) == -1):  # imfotmation[1]是朋友的名称
                # 发送的消息如果失败了
                playsound.playsound("../SystemSpeech/service/contractNotFound.mp3")
            else:
                playsound.playsound("../SystemSpeech/Skype/sendSuccess.mp3")
        elif  "播放音乐"  in command or "播放歌曲" in  command:
            self.oldValue = 0
            playsound.playsound("../SystemSpeech/music/musicNameRequired.mp3")
            record_vad.record_vad("../SystemSpeech/music/musicName.wav",40)
            musicName=speech.asr(get_file_content("../SystemSpeech/music/musicName.pcm"),'pcm',16000,{
                "dev_pid":1537
            })['result'][0]
            print("歌曲名：",musicName.split("。")[0])
            self.player.set_uri(music.searchNetMusic(musicName.split("。")[0])  )#搜索同时播放音乐，去除识别产生的句号，实际也可以不去除
            self.player.play()
            return
        elif "暂停播放" in command:
            #音乐进程不为空 音乐进程仍然在播放
            if not self.player.playing_uri=="":
               #仍然在播放音乐的话
               playsound.playsound("../SystemSpeech/service/Idoit.mp3")
               self.oldValue=0         # 告知，已修改
        elif "继续播放"  in command:
            # 音乐进程不为空，音乐进程没有被杀死 音乐暂停播放
            if not self.player.playing_uri=="": # 仍然在播放音乐的话
                playsound.playsound("../SystemSpeech/service/Idoit.mp3")
                self.player.resume()
                self.oldValue=0
        elif "停止播放" in command:

            if not self.player.playing_uri=="" :
                playsound.playsound("../SystemSpeech/service/Idoit.mp3")
                self.player.stop()
                self.oldValue=0

        elif "增大音量" in command or "大声点" in command:
            # 如果在播放音乐，等等，实际上似乎用不上消息队列
            # 如果在播放音乐，增加音乐音量
            playsound.playsound("../SystemSpeech/service/Idoit.mp3")
            if self.player.is_playing():
                self.player.add_volume()
            else :
                #  TODO 如果没有播放音乐，则增加音箱音量  MAC端 迁移到树莓派时需要修正
                pass
        elif "减小音量" in command or "小声点" in command:
            # 如果在播放音乐，等等，实际上似乎用不上消息队列
            # 如果在播放音乐，减小音乐音量
            playsound.playsound("../SystemSpeech/service/Idoit.mp3") # 好的
            if not self.player.playing_uri=="":
                self.player.sub_volume()   # 此处测试不通过消息队列处理
            else:
                pass
                #  TODO 如果没有播放音乐，则减少音箱音量  MAC端 迁移到树莓派时需要修正
                #  TODO 暂时没有修正方案


if __name__=="__main__":
    record_vad.record_vad("smallchat.wav", 50)  # 产生一个smallchat.pcm文件在底层
    speech = AipSpeech(APP_ID, APP_KEY, SECRET_KEY)
    p = speech.asr(get_file_content('smallchat.pcm'), 'pcm', 16000, {
        'dev_pid': 1537,
    })
    command = p['result'][0]  # 从json中提取识别出来的文字
    print(command)





