# -*- coding: utf-8 -*-
import re
import sys
import logging
import json
import time
import requests

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


# 读取配置
def get_config():
    with open("./config.json", 'r') as f:
        load_dict = json.load(f)
    return load_dict


# 登录，为后续做准备
def login(s, username, password, timeout, headers):
    login_url = 'http://yiqing.ctgu.edu.cn/wx/index/loginSubmit.do'
    data = {'username': username, 'password': password}
    r = s.post(url=login_url, data=data, timeout=timeout, headers=headers)
    if r.text == 'success':
        return True


# 退出登录
def logout(s, headers):
    logout_url = 'http://yiqing.ctgu.edu.cn/wx/index/logout.do'
    s.get(url=logout_url, headers=headers)


# 获取要带有data的html
def get_student_info(s, headers):
    student_info_url = 'http://yiqing.ctgu.edu.cn/wx/health/toApply.do'
    r = s.get(url=student_info_url, headers=headers)
    return r.text


# 解析html,获得data数据
def student_info_parse(html):
    if len(re.findall(r'name="ttoken" value="(.*?)"/>', html)) == 0:
        return False
    data = {
        'ttoken': re.findall(r'name="ttoken" value="(.*?)"/>', html)[0],  # ttoken
        'province': re.findall(r'name="province" id="province" value="(.*?)"/>', html)[0],  # 省
        'city': re.findall(r'name="city" id="city" value="(.*?)"/>', html)[0],  # 市
        'district': re.findall(r'name="district" id="district" value="(.*?)"/>', html)[0],  # 县
        'adcode': re.findall(r'name="adcode" id="adcode" value="(.*?)"/>', html)[0],  # 邮编
        'longitude': re.findall(r'name="longitude" id="longitude" value="(.*?)"/>', html)[0],  # 经度
        'latitude': re.findall(r'name="latitude" id="latitude" value="(.*?)"/>', html)[0],  # 纬度
        'sfqz': '否',
        'sfys': '否',
        'sfzy': '否',
        'sfgl': '否',
        'status': re.findall(r'name="status" id="status" value="(.*?)"/>', html)[0],
        'szdz': re.findall(r'name="szdz"  maxlength="20" value="(.*?)" readonly>', html)[0],  # 所在地区
        'sjh': re.findall(r'name="sjh" maxlength="20" value="(.*?)">', html)[0],  # 手机号
        'lxrxm': re.findall(r'name="lxrxm" maxlength="40" value="(.*?)"', html)[0],  # 紧急联系人姓名
        'lxrsjh': re.findall(r'name="lxrsjh" maxlength="40" value="(.*?)"', html)[0],  # 紧急联系人电话
        'sffr': '否',
        'sffrAm': '否',
        'sffrNoon': '否',
        'sffrPm': '否',
        'sffy': '否',
        'sfgr': '否',
        'qzglsj': '',
        'qzgldd': '',
        'glyy': '',
        'mqzz': '',
        'sffx': '否',
        'qt': '',
    }
    return data


# 向服务器post数据
def sent_info(s, data, headers):
    sent_info_url = 'http://yiqing.ctgu.edu.cn/wx/health/saveApply.do'
    r = s.post(url=sent_info_url, data=data, headers=headers)
    result = json.loads(r.text)
    return result['msgStatus'] == 'true'


# 推送消息
def push_msg(msg, token):
    pushplus_url = 'http://pushplus.hxtrip.com/send'
    data = {
        'token': token,
        'title': '每日报平安通知',
        'content': msg,
        'template': 'html'
    }
    r = requests.post(url=pushplus_url, data=data)
    result = json.loads(r.text)
    if result['code'] == 200:
        logger.info('消息发送成功')


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }

    # 配置文件
    config = get_config()
    users = config['users']
    timeout = config['timeout']
    pushplus_token = config['pushplus_token']
    push_level = config['push_level']
    wait_time = config['wait_time']

    total = len(users)
    finished = 0
    detail_msg = ''
    start_time = time.time()
    for i in range(total):
        # 报一个等待时间
        time.sleep(wait_time)
        s = requests.Session()
        # 尝试登录
        try:
            flag = login(s, str(users[i][0]), str(users[i][1]), timeout, headers)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            s.close()
            logger.info(str(users[i][0]) + ':登录超时')
            detail_msg += str(users[i][0]) + ':登录超时<br>'
            if len(users[i]) == 3 and users[i][2] != '':
                push_msg('自动上报平安失败，登录超时', users[i][2])
            continue
        # 登录成功
        if flag:
            # logger.info(str(users[i][0]) + ':登录成功')
            html = get_student_info(s, headers)
            data = student_info_parse(html)
            # 今日已上报
            if not data:
                logout(s, headers)
                s.close()
                finished += 1
                logger.info(str(users[i][0]) + ':今日已上报')
                detail_msg += str(users[i][0]) + ':今日已上报<br>'
                continue
            # 上报成功
            if sent_info(s, data, headers):
                logout(s, headers)
                s.close()
                logger.info(str(users[i][0]) + ':上报成功')
                detail_msg += str(users[i][0]) + ':上报成功<br>'
                finished += 1
            # 上报失败
            else:
                logout(s, headers)
                s.close()
                logger.info(str(users[i][0]) + ':上报失败')
                detail_msg += str(users[i][0]) + ':上报失败<br>'
                if len(users[i]) == 3 and users[i][2] != '':
                    push_msg('自动上报平安失败，服务异常', users[i][2])
                continue
        # 登录失败
        else:
            s.close()
            logger.info(str(users[i][0]) + ':密码错误，登录失败')
            detail_msg += str(users[i][0]) + ':密码错误<br>'
            if len(users[i]) == 3 and users[i][2] != '':
                push_msg('自动上报平安失败，请检查密码', users[i][2])
            continue

    endtime = time.time()
    usedtime = "%.3f" % (endtime - start_time)

    # 注意，这里云函数时间不是北京时间，需要加8小时
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800))
    # nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    logger.info(nowtime+'  应报:'+str(total)+' 实报:'+str(finished)+' 用时:'+usedtime)

    detail_msg = nowtime+'<br>应报:'+str(total)+' 实报:'+str(finished)+' 用时:'+usedtime+'<br>'+detail_msg

    # 根据推送等级推送
    if push_level == 1:
        push_msg(detail_msg, pushplus_token)
    elif push_level == 2:
        push_msg(nowtime+'<br>应报:'+str(total)+' 实报:'+str(finished)+' 用时:'+usedtime, pushplus_token)
    elif push_level == 3:
        if total != finished:
            push_msg(detail_msg, pushplus_token)
    elif push_level == 4:
        if float(finished/total) < 0.9:
            push_msg(detail_msg, pushplus_token)
    elif push_level == 5:
        if float(finished/total) < 0.5:
            push_msg(detail_msg, pushplus_token)


def main_handler(event, content):
    logger.info('-'*20+'日志分界线'+'-'*20)
    main()
    logger.info('-'*20+'日志分界线'+'-'*20)


# main()
