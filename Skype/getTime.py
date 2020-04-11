import time

def getFullTime():
    nowTime=time.localtime()
    ChineseTime=""
    ChineseTime+=str(nowTime.tm_year)
    ChineseTime+="年"
    ChineseTime+=str(nowTime.tm_mon)
    ChineseTime+="月"
    ChineseTime+=str(nowTime.tm_mday)
    ChineseTime+="日"
    ChineseTime+="周"
    if(nowTime.tm_wday==7 ):
        ChineseTime+="日  "
    else:
        ChineseTime+=str(nowTime.tm_wday)
        ChineseTime+= " "
    ChineseTime+=str(nowTime.tm_hour)
    ChineseTime+="点"
    ChineseTime+=str(nowTime.tm_min)
    ChineseTime+="分"
    ChineseTime+=str(nowTime.tm_sec)
    ChineseTime+="秒"
    return ChineseTime
def getFulldate():
    nowTime = time.localtime()
    ChineseTime = ""
    ChineseTime += str(nowTime.tm_year)
    ChineseTime += "年"
    ChineseTime += str(nowTime.tm_mon)
    ChineseTime += "月"
    ChineseTime += str(nowTime.tm_mday)
    ChineseTime += "日"
    ChineseTime += "周"
    if (nowTime.tm_wday == 7):
        ChineseTime += "日  "
    else:
        ChineseTime += str(nowTime.tm_wday)
        ChineseTime += " "
    return ChineseTime
def getTime():
    nowTime = time.localtime()
    ChineseTime = ""
    ChineseTime += str(nowTime.tm_hour)
    ChineseTime += "点"
    ChineseTime += str(nowTime.tm_min)
    ChineseTime += "分"
    ChineseTime += str(nowTime.tm_sec)
    ChineseTime += "秒"
    return ChineseTime

if __name__ =='__main__':
    print(getTime())