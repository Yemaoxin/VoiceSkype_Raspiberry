from aip import AipSpeech
## api接口的参数，账号
APP_ID="18754384"
APP_KEY="VjxtYrtYNaN7RIchnj0MfE7H"
SECRET_KEY="VyXqlikq1LNnDd2cQ9sfwQO2ghGFenWZ"

def Synthesis(string,path='../Hardware/auido.mp3'):
    app=AipSpeech(APP_ID,APP_KEY,SECRET_KEY)
    result = app.synthesis(string, 'zh', 1, {
        'vol': 5,
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(path, 'wb') as f:
            f.write(result)

if __name__ =="__main__":
    # Synthesis("开始设置声音，请重复三遍小瓜小瓜","../SystemSpeech/start_set.mp3")
    # Synthesis("第一遍，请说小瓜小瓜", "../SystemSpeech/start_set1.mp3")
    # Synthesis("请再说一次小瓜小瓜", "../SystemSpeech/start_set2.mp3")
    # Synthesis("最后再说一次小瓜小瓜", "../SystemSpeech/start_set3.mp3")
    # Synthesis("我在", "../SystemSpeech/do.mp3")
    # Synthesis("天气定位服务异常","../SystemSpeech/weather/ipLocationError.mp3")
    # Synthesis("请直接告知所在地","../SystemSpeech/weather/locationRequire.mp3")
    # Synthesis("进入闲聊模式", "../SystemSpeech/service/start_chat.mp3")
    # Synthesis("退出闲聊模式", "../SystemSpeech/service/end_chat.mp3")
    Synthesis("好的", "../SystemSpeech/service/Idoit.mp3")