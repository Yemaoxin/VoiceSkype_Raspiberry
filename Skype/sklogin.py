from skpy import  *
from Constants  import Constants
from SkLog import Sklog

log=Sklog()


def login():
    contacts = {}
    retryCount=0
    while (retryCount<Constants.retryLimit):
        try:
            account = Skype("1648428830@qq.com", "123456789ymx")
            ## 为啥获取到的数据却没法子取出来
            ## 只能保存到本地，而且需要从raw数据中取出
            # account.contacts['jh'].cha
            for i in account.contacts:
                name = i.raw["display_name"]
                contacts[name] = i
        except Exception as  e:
            log.warning("网络问题，请检查网络链接")
            return -1, -1
        return account, contacts


if __name__=="__main__":
    c=login()

    # c['jh'].chat.sendMsg("你在干嘛呀小姐姐")













