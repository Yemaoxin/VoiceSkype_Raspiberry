import requests
import json
import sys
sys.path.append("..")
from Speech import SpeechSynthesis
import logging
from playsound import playsound
key="788ac9d7b6100df59442f5abf8cbcc85"
log=logging.getLogger("天气服务")

def getWeather(date=0,city=""):
    """
    此处是天气查询包含：
    1、未指定时间和地点
    2、指定明天，不指定地点
    3、指定地点，不指定时间
    4、均指定
    手机端或小程序api则会提供更精确的定位。
    默认utf-8编码
    :return:  天气情况 ，异常时返回-1
    """
    if(city!=""):     # 设置城市
        city_url = "https://restapi.amap.com/v3/config/district?key=" + key
        city_url += "&keywords=" + city + "&subdistrict=0&extensions=base"
        city_content = requests.get(city_url).json()
        adcode = city_content['districts'][0]["adcode"]
        weather_url = r"https://restapi.amap.com/v3/weather/weatherInfo?key=" + key
        weather_url = weather_url + "&city=" + adcode
        if date==1:
            weather_url+="&extensions=all"
            information=requests.get(weather_url).json()
            return jointCast(information)
        weather_content = requests.get(weather_url).json()
        weather_condition = weather_content['lives'][0]
        return joint(weather_condition)
    else:
        ip_url = "https://restapi.amap.com/v3/ip?" + "key=" + key
        weather_url = r"https://restapi.amap.com/v3/weather/weatherInfo?key=" + key
        content = requests.get(ip_url).json()
        if (content["status"] != "1"):
            log.warning("定位服务异常")
            return -1
        else:
            adcode = content["adcode"]
            log.info("服务定位ascode：" + adcode)
            weather_url = weather_url + "&city=" + adcode
            if (date == 1):  # 选取第二天数据
                weather_url += "&extensions=all"
                imformation=requests.get(weather_url).json()
                return jointCast(imformation)
            weather_content = requests.get(weather_url).json()
            weather_condition = weather_content['lives'][0]
            return joint(weather_condition)


def  joint(condition):
    """
    拼接天气信息
    :param condition: 一个天气信息的字典
    :return: 转化为可读的字符串
    """
    string=condition["province"]+"省"
    string+=condition['city']
    string+=",天气,"+condition['weather']
    string+=",气温,"+condition['temperature']+"摄氏度"
    string+=",风向,"+condition["winddirection"]
    string+=",风力,"+condition["windpower"]
    string+=",湿度,"+condition['humidity']
    return string

def  jointCast(cast):
    if cast['status']!='1':
        return -1
    information=cast['forecasts'][0]
    cast=information['province']
    cast+="省"
    cast+=information['city']
    cast+=",明天白天"
    cast+=information['casts'][1]['dayweather']
    cast+=",白天温度"
    cast+=information['casts'][1]['daytemp']
    cast+="度"
    cast+=',明天晚上'
    cast+=information['casts'][1]['nightweather']
    cast+=',晚上温度'
    cast+=information['casts'][1]['nighttemp']
    cast += "度"
    return cast

if __name__ == "__main__" :
    log.warning(getWeather(date=1,city="厦门"))
