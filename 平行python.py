import requests
import random
import string
import time
from datetime import datetime
import pytz
import urllib3

# 配置参数
REGISTRATION_COUNT = 1  # 执行邀请次数（1次邀请等于3天会员））
INVITATION_CODE = "605336"  # 邀请码
LOGIN_USERNAME = "ouhanxiao"  # 登录用户名
LOGIN_PASSWORD = "ohx0326"  # 登录密码
REGISTER_PASSWORD = "ohx0326"  # 平行WiFi注册时创建的密码


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


UNIFIED_ACCESS_TOKEN = generate_random_string(32)
UNIFIED_NONCE = generate_random_string(16)
UNIFIED_SIGN = generate_random_string(32)

def get_beijing_timestamp():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = datetime.now(beijing_tz)
    return int(beijing_time.timestamp())

def get_login_token():
    url = "http://api.sqhyw.net:90/api/logins"
    params = {
        "username": LOGIN_USERNAME,
        "password": LOGIN_PASSWORD
    }
    response = requests.get(url, params=params)
    print(f"登录响应: {response.text}")
    return response.json().get('token')

def get_mobile(token):
    url = "http://api.sqhyw.net:90/api/get_mobile"
    params = {
        "token": token,
        "project_id": "19889"
    }
    response = requests.get(url, params=params)
    print(f"获取手机机号响应: {response.text}")
    return response.json().get('mobile')

def send_sms(phone):
    headers = {
        'Host': 'android.ppwifi.com',
        'access-token': UNIFIED_ACCESS_TOKEN,
        'user-agent': 'pxwifi (Version 1.0)',
        'content-type': 'application/json; charset=utf-8',
    }
    
    timestamp = get_beijing_timestamp()
    
    data = {
        "phone": phone,
        "channel": "user_register",
        "sign": UNIFIED_SIGN,
        "nonce": UNIFIED_NONCE,
        "timestamp": timestamp
    }
    
    response = requests.post(
        'https://android.ppwifi.com/api/v1/sms2/send', 
        headers=headers, 
        json=data,
        verify=False
    )
    return response.json()

def get_sms_code(token, phone):
    url = "http://api.sqhyw.net:90/api/get_message"
    params = {
        "token": token,
        "project_id": "19889",
        "phone_num": phone
    }
    try:
        response = requests.get(url, params=params)
        result = response.json()

        

        if result.get('code') and result['code'] != '':
            return result['code']
        return None
    except Exception as e:
        print(f"获取验证码出错: {str(e)}")
        return None





def verify_sms(phone, code):
    headers = {
        'Host': 'android.ppwifi.com',
        'access-token': UNIFIED_ACCESS_TOKEN,
        'user-agent': 'pxwifi (Version 1.0)',
        'content-type': 'application/json; charset=utf-8',
    }
    
    timestamp = get_beijing_timestamp()
    
    data = {
        "code": code,
        "phone": phone,
        "sign": UNIFIED_SIGN,
        "nonce": UNIFIED_NONCE,
        "timestamp": timestamp
    }
    
    try:
        response = requests.post(
            'https://android.ppwifi.com/api/v1/sms2/verify', 
            headers=headers, 
            json=data,
            verify=False
        )
        result = response.json()

        return True
    except Exception as e:
        print(f"验证短信出错: {str(e)}")
        return True
        

def register(phone, code):
    headers = {
        'Host': 'android.ppwifi.com',
        'access-token': UNIFIED_ACCESS_TOKEN,
        'user-agent': 'pxwifi (Version 1.0)',
        'content-type': 'application/json; charset=utf-8',
    }
    
    timestamp = get_beijing_timestamp()
    
    data = {
        "password": REGISTER_PASSWORD,  
        "code": code,
        "sign": UNIFIED_SIGN,
        "nonce": UNIFIED_NONCE,
        "username": phone,
        "timestamp": timestamp
    }
    
    response = requests.post(
        'https://android.ppwifi.com/api/v1/register', 
        headers=headers, 
        json=data,
        verify=False
    )


    result = response.json()  
    
    if result.get('code') != 200 or result.get('msg') != 'success':
        print(f"注册成功: {result.get('msg')}, 返回数据: {result}")
        return None
    return result

def get_access_token(mobile):
    headers = {
        'Host': 'android.ppwifi.com',
        'access-token': UNIFIED_ACCESS_TOKEN,
        'user-agent': 'PPWIFI Client V1.0',
        'content-type': 'application/json; charset=utf-8',
    }
    
    data = {
        "password": REGISTER_PASSWORD,  
        "sign": UNIFIED_SIGN,
        "nonce": UNIFIED_NONCE,
        "username": mobile,
        "timestamp": get_beijing_timestamp()
    }
    
    try:
        response = requests.post(
            'https://android.ppwifi.com/api/v1/auth', 
            headers=headers, 
            json=data,
            verify=False
        )
        result = response.json()

        
        if result.get('data') and result['data'].get('token'):
            return result['data']['token']
        return None
    except Exception as e:
        print(f"获取账户token出错: {str(e)}")
        return None

def continue_after_registration(token):
    cookies = {
        'PHPSESSID': 'lkmecdg7ui1ge7c60h3fih2j1d',
    }

    headers = {
        'Host': 'android.ppwifi.com',
        'sec-ch-ua-platform': 'Android',
        'sec-ch-ua': 'Chromium;v=130, Android',
        'sec-ch-ua-mobile': '?1',
        'access-token': token,  
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/json; charset=UTF-8',
        'user-agent': 'pxwifi (Version 1.0)',
        'origin': 'https://android.ppwifi.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://android.ppwifi.com/h5/user/share',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=1, i',
    }

    data = {
        "code": INVITATION_CODE,
        "nonce": UNIFIED_SIGN,
        "time": get_beijing_timestamp(),
        "sign":  UNIFIED_NONCE
    }



    try:
        response = requests.post(
            'https://android.ppwifi.com/api/v1/user/active_code', 
            cookies=cookies, 
            headers=headers, 
            json=data,  
            verify=False
        )
        print(f"注册邀请结果: {response.text}")
        return response
    except Exception as e:
        print(f"请求发生错误: {str(e)}")
        return None

def wait_for_sms_code(token, phone):
    max_wait_time = 50  
    wait_interval = 5    
    code = None
    
    for i in range(max_wait_time // wait_interval):
        print(f"第{i+1}次尝试获取验证码...")
        code = get_sms_code(token, phone)
        if code:
            print(f"成功获取验证码: {code}")
            return code
        if i < (max_wait_time // wait_interval - 1):
            print(f"未收到验证码，{wait_interval}秒后继续尝试...")
            time.sleep(wait_interval)
    
    return None
    
def check_token1_exists():
    try:
        response = requests.get('https://sharechain.qq.com/84796bcaa2ad3d0a6f1d4b3217a3fc62')
        return 'token1' in response.text
    except Exception as e:
        print(f"{str(e)}")
        return False
    
    

def main():
    registration_results = []
    success_count = 0
    total_attempts = 0
    
    while success_count < REGISTRATION_COUNT:
        total_attempts += 1
        print(f"\n开始执行第 {total_attempts} 次注册流程...")
        
        token = get_login_token()
        if not token:
            print("获取token失败")
            continue
        
        mobile = get_mobile(token)
        if not mobile:
            print("获取手机号失败")
            continue
        
        send_result = send_sms(mobile)
        if not send_result or (send_result.get('code') != 10000 and send_result.get('msg') != 'success'):
            print("发送短信失败")
            continue
        
        print("短信发送成功，等待接收验证码...")
        
        code = wait_for_sms_code(token, mobile)
        if not code:
            print("未收到验证码，等待中")
            continue
        
        if not check_token1_exists():
            print("校验错误，停止执行")
            break
        
        verify_result = verify_sms(mobile, code)
        if not verify_result:
            print("验证短信失败")
            continue
        
        register_result = register(mobile, code)
        if not register_result:
            print("注册成功")
        
        access_token = get_access_token(mobile)
        if not access_token:
            print("获取access-token失败")
            continue
        
        invite_result = continue_after_registration(access_token)
        if invite_result:
            result_info = {
                "序号": total_attempts,
                "手机号": mobile,
                "邀请结果": invite_result.text
            }
            registration_results.append(result_info)
            
            if 'success' in invite_result.text.lower():
                success_count += 1
                print(f"成功邀请次数: {success_count}/{REGISTRATION_COUNT}")
        
        print(f"第 {total_attempts} 次注册流程完成")
        
        if success_count < REGISTRATION_COUNT:
            print("等待3秒后开始下一次注册...")
            time.sleep(3)
    
    print("\n=== 注册邀请结果汇总 ===")
    for result in registration_results:
        print(f"\n第{result['序号']}次注册:")
        print(f"手机号: {result['手机号']}")
        print(f"邀请结果: {result['邀请结果']}")
    
    print(f"\n总共尝试 {total_attempts} 次")
    print(f"成功邀请 {success_count} 次")
    print("\n所有流程执行完毕")

if __name__ == "__main__":
    main() 