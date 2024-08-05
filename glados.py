import requests,json,os
import urllib.parse
import urllib.request

# -------------------------------------------------------------------------------------------
# SERVER酱
# -------------------------------------------------------------------------------------------
def sc_send(text, desp='', key='[SENDKEY]'):
    postdata = urllib.parse.urlencode({'text': text, 'desp': desp}).encode('utf-8')
    url = f'https://sctapi.ftqq.com/{key}.send'
    req = urllib.request.Request(url, data=postdata, method='POST')
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
    return result


# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
# pushplus秘钥 申请地址 http://www.pushplus.plus
    sckey_push = os.environ.get("PUSHPLUS_TOKEN", "")

# Server酱 申请地址 https://sct.ftqq.com/sendkey
    sckey_server = os.environ.get("SERVER_KEY", "")

# 推送内容
    sendContent = ''
# glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("GLADOS_COOKIE", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量') 
        cookies = []
        exit(0)
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload={
        'token': 'glados.one'
    }
    for cookie in cookies:
        checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    #--------------------------------------------------------------------------------------------------------#  
        time = state.json()['data']['leftDays']
        time = str(time).split('.')[0]
        email = state.json()['data']['email']
        if 'message' in checkin.text:
            mess = checkin.json()['message']
            print("签到成功") # 日志输出
            # print(email+'----结果--'+mess+'----剩余('+time+')天')  # 日志输出
            sendContent += email+'----'+mess+'----剩余('+time+')天\n'
        else:
            if sckey_push != "":
                requests.get('http://www.pushplus.plus/send?token=' + sckey_push + '&content='+email+'cookie已失效')
            if sckey_server != "":  
                sc_send('cookie已失效', email+'cookie已失效', sckey_server)
            print('cookie已失效')  # 日志输出
     #--------------------------------------------------------------------------------------------------------#   
    if sckey_push != "":
        requests.get('http://www.pushplus.plus/send?token=' + sckey_push + '&title='+email+'签到成功'+'&content='+sendContent)
    if sckey_server != "":
        print("Server酱请求")
        ret = sc_send(email, sendContent, sckey_server)
        


