"""
  腾讯的API接口对数据有比较多的要求
  1、sign签名
  2、字典升序
  3、md5加密
  4、全部转大写
  5、遗漏点：value值要进行url编码，而且是大写的
"""
import hashlib
import urllib.parse
import requests
import json
import time
import random
import string
app_id="2130944758"
app_key="LGcjMhNMuD8wsYFI"
url="https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat?"
import playsound

def getSign(data={}):
    """
    按照要求进行进行数据签名
    params = array(
    'app_id'     => '10000',
    'time_stamp' => '1493449657',
    'nonce_str'  => '20e3408a79',
    'key1'       => '腾讯AI开放平台',
    'key2'       => '示例仅供参考',
    'sign'       => '',
    );
1、将<key, value>请求参数对按key进行字典升序排序，得到有序的参数对列表N
2、将列表N中的参数对按URL键值对的格式拼接成字符串，得到字符串T（如：key1=value1&key2=value2），URL键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8，而不是小写%e8
3、将应用密钥以app_key为键名，组成URL键值拼接到字符串T末尾，得到字符串S（如：key1=value1&key2=value2&app_key=密钥)
4、对字符串S进行MD5运算，将得到的MD5值所有字符转换成大写，得到接口请求签名
    注意就是sign不加入计算
    :param data: 参数列表
    :return: 加密结果sign签名
    """
    # 字母表升序
    data=sorted(data.items())

    # 拼接字符串
    dataStr=''
    for i in data:
        if(i[1]!=""):
          dataStr+=i[0]
          dataStr+="="
          dataStr+=urllib.parse.quote(str(i[1]),encoding='utf-8')
          dataStr += "&"

    # 加入密钥
    dataStr+="app_key="
    dataStr+=app_key

    # md5加密 转大写
    hash=hashlib.md5()      #md5
    dataStr=hash.update(dataStr.encode(encoding="utf-8"))
    dataStr=hash.hexdigest()  #转为hex十六进制大写
    return dataStr.upper()       #大写

def doHttpGet(data={}):
    """
    发送http请求到腾讯服务器
    在函数内部完成字符串拼接
    :param data:参数列表
    :return:
    """
    chat_url=url
    if data['sign']=='':
        return -1
    num=0
    for i in data.items():
        if num!=0:
          chat_url+='&'
        num+=1
        chat_url+=i[0]
        chat_url+="="
        chat_url+=str(i[1])
    data=requests.get(chat_url)
    return data.json()

def sendQuestion(question=""):
    data={}
    data['app_id']=app_id
    data["time_stamp"]=str(int(time.time()))
    data['nonce_str']="".join(random.sample(string.ascii_letters+string.digits,10))  #随机生成20个字符
    data['session']=10000          #暂时不明白这个是什么唯一，应该是对于一个应用内部的多个客户端而言
    data['sign']=""
    data['question']=question
    sign=getSign(data)
    data['sign']=sign
    response=doHttpGet(data)
    print(response)
    if(not  response['ret']==0):
        playsound.playsound('SystemSpeech/service/sorry.mp3')
    else:
        return  response['data']['answer']


if __name__=='__main__':
    print(sendQuestion("你喜欢干啥"))






