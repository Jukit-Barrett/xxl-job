#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
from datetime import datetime


def dump(params):
    resp = json.dumps(params, indent=4, ensure_ascii=False)
    print(resp)


def current_date() -> str:
    # 获取当前时间
    current_time = datetime.now()
    # 格式化输出：年月日 时分秒
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


def build_resp(code, msg, data: dict | None) -> dict:
    return {
        'code': int(code),
        'msg': str(msg),
        'data': data,
    }


def get(url: str, headers: dict, payload: dict) -> dict:
    response = None  # 初始化变量，避免未赋值引用
    try:
        response = requests.get(url, headers=headers, data=payload, verify=False)
        response.raise_for_status()  # 触发HTTP错误（4xx/5xx状态码）
        resp = response.json()
        return resp
    except requests.exceptions.HTTPError as e:
        status_code = response.status_code if response is not None else 500
        return build_resp(status_code, f"HTTP请求失败: {str(e)}", {"status_code": status_code})

    except requests.exceptions.ConnectionError as e:
        return build_resp(9991, f"连接服务器失败: {str(e)}", None)

    except requests.exceptions.Timeout as e:
        return build_resp(9992, f"请求超时: {str(e)}", None)

    except Exception as e:
        return build_resp(9999, f"请求处理异常: {str(e)}", None)


def post(url: str, headers: dict, payload: dict) -> dict:
    response = None  # 初始化变量，避免未赋值引用
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()  # 触发HTTP错误（4xx/5xx状态码）
        resp = response.json()
        return resp
    except requests.exceptions.HTTPError as e:
        status_code = response.status_code if response is not None else 500
        return build_resp(status_code, f"HTTP请求失败: {str(e)}", {"status_code": status_code})

    except requests.exceptions.ConnectionError as e:
        return build_resp(9991, f"连接服务器失败: {str(e)}", None)

    except requests.exceptions.Timeout as e:
        return build_resp(9992, f"请求超时: {str(e)}", None)

    except Exception as e:
        return build_resp(9999, f"请求处理异常: {str(e)}", None)


def tool_sys_login():
    url = f"http://javagod.dev.cychan.site/ibk/god/auth/login"
    headers = {
    }
    payload = {
        "username": "jukit",
        "password": "123456",
    }
    return post(url, headers, payload)


def tool_sys_ping():
    url = f"http://javagod.dev.cychan.site/ibk/god/test/ping"
    headers = {
    }
    payload = {
    }
    return get(url, headers, payload)


if __name__ == '__main__':
    resp = tool_sys_ping()
    dump(resp)
