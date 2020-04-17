import sys
sys.path.append('..')
from skpy import Skype,SkypeEventLoop, SkypeNewMessageEvent,SkypeUser
import requests
import multiprocessing
import os
from Speech import SpeechSynthesis
from playsound import playsound
class SkypeCustomEventLoop(Skype):
    """
    A skeleton class for producing event processing programs.  Implementers will most likely want to override the
    :meth:`onEvent` method.

    Attributes:
        autoAck (bool):
            Whether to automatically acknowledge all incoming events.
    """

    attrs = Skype.attrs + ("autoAck",)

    def __init__(self, user=None, pwd=None, tokenFile=None, autoAck=True, status=None):
        """
        Create a new event loop and the underlying connection.

        All arguments up to ``tokenFile``  are passed to the :class:`.SkypeConnection` instance.

        Args:
            user (str): Skype username of the connecting account
            pwd (str): corresponding Skype account password
            tokenFile (str): path to file used for token storage
            autoAck (bool): whether to automatically acknowledge all incoming events
            status (.Status): availability to display to contacts
        """
        super().__init__(user, pwd, tokenFile)
        self.autoAck = autoAck
        if status:
            self.setPresence(status)

    def cycle(self):
        """
        Request one batch of events from Skype, calling :meth:`onEvent` with each event in turn.

        Subclasses may override this method to alter loop functionality.
        """
        try:
            events = self.getEvents()
        except requests.ConnectionError:
            return
        for event in events:
            self.onEvent(event)
            if self.autoAck:
                event.ack()

    def loop(self):
        """
        Continuously handle any incoming events using :meth:`cycle`.

        This method does not return, so for programs with a UI, this will likely need to be run in its own thread.
        """
        while True:
            self.cycle()

    def onEvent(self, event):
        """
        A stub method that subclasses should implement to react to messages and status changes.

        Args:
            event (SkypeEvent): an incoming event
        """
        pass

class SkypePing(SkypeCustomEventLoop):
    def __init__(self,username,password):
        super(SkypePing, self).__init__(username,password)
    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) \
          and not event.msg.userId == self.userId :
            message_describe=event.msg.user.raw
            friend_name=message_describe['display_name']     # 获取好友的名称
            message_detail="你的好友"+friend_name+"发来一条消息,"+event.msg.content
            SpeechSynthesis.Synthesis(message_detail,"../SystemSpeech/Skype/newMessage.mp3")
            # if(self.Queue.full()):
            #     self.Queue.get()    # 暂时没有使用消息队列的需要
            # self.Queue.put(friend_name)
            try:
              playsound.playsound("../SystemSpeech/Skype/newMessage.mp3")
              #存在有音频占用的可能性
            except Exception as e:
                print(e)
                playsound.playsound("../SystemSpeech/Skype/newMessage.mp3")

    def getContacts(self):
        """
        将self的联系人换成用通用名的字典联系人形式
        :return:
        """
        friends={}
        for i in self.contacts:
            name = i.raw["display_name"]
            friends[name] = i
        return friends
    def getFriends(self):
        return self.getContacts()


def run(ping):
    ping.loop()


if __name__ =="__main__" :

    print(os.getpid())
    ping = SkypePing("1648428830@qq.com", "123456789ymx")
    friends = ping.getFriends()
    multiprocessing.Process(target=run,args=(ping,)).start()
    import time
    time.sleep(15)
    friends['二弟'].chat.sendMsg('cbhjaclkdmv fjnabhsbjcbajsnjks')