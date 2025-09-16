import requests
import random
import string
import json


def dump(json_params):
    dump_ret = json.dumps(json_params, indent=4, ensure_ascii=False)
    print(dump_ret)


def build_resp(code, msg, data: dict | None) -> dict:
    return {
        'code': int(code),
        'msg': str(msg),
        'data': data,
    }


def generate_random_string(
        length=10,
        include_uppercase=True,
        include_lowercase=True,
        include_digits=True,
        include_special_chars=False
):
    # 构建字符集
    char_set = ''

    if include_uppercase:
        char_set += string.ascii_uppercase  # A-Z
    if include_lowercase:
        char_set += string.ascii_lowercase  # a-z
    if include_digits:
        char_set += string.digits  # 0-9
    if include_special_chars:
        # 可根据需求调整特殊字符集
        char_set += '!@#$%^&*()_-+=[]{}|;:,.<>?`~'

    # 验证至少选择了一种字符类型
    if not char_set:
        raise ValueError("至少需要启用一种字符类型")

    # 验证长度为正整数
    if length <= 0:
        raise ValueError("长度必须为正整数")

    # 生成随机字符串
    return ''.join(random.choice(char_set) for _ in range(length))


class XXLJob():
    def __init__(self, url: str, token: str | None = None):
        self.url = url
        self.token = token
        if self.token is not None:
            self.headers = self.build_headers(token)
        else:
            self.headers = {}

    def build_headers(self, token) -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Cookie": f"xxl_job_login_token=" + token,
        }

    def post(self, url: str, headers: dict, payload: dict) -> dict:
        response = None  # 初始化变量，避免未赋值引用
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # 触发HTTP错误（4xx/5xx状态码）
            resp = response.json()
            return build_resp(resp.get("code"), resp.get("msg"), resp.get("content"))
        except requests.exceptions.HTTPError as e:
            status_code = response.status_code if response is not None else 500
            return build_resp(status_code, f"HTTP请求失败: {str(e)}", {"status_code": status_code})

        except requests.exceptions.ConnectionError as e:
            return build_resp(9991, f"连接服务器失败: {str(e)}", None)

        except requests.exceptions.Timeout as e:
            return build_resp(9992, f"请求超时: {str(e)}", None)

        except Exception as e:
            return build_resp(9999, f"请求处理异常: {str(e)}", None)

    # 登陆
    def login(self, username: str, password: str) -> dict | None:
        request_url = self.url + f"/xxl-job-admin/auth/doLogin"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        }
        payload = {
            "userName": username,
            "password": password,
            "ifRemember": "on"
        }

        response = self.post(request_url, headers=headers, payload=payload)
        token = response.get("data")
        self.token = token
        self.headers = self.build_headers(token)
        return build_resp(response.get("code"), response.get("msg"), {"token": token})

    # 报表接口
    def chart_info(self):
        request_url = self.url + f"/xxl-job-admin/chartInfo"
        headers = self.headers
        payload = {
            "startDate": "2025-09-03 00:00:00",
            "endDate": "2025-09-10 23:59:59",
        }

        return self.post(request_url, headers=headers, payload=payload)

    # 添加任务
    def job_add(self, params: dict):
        payload = {
            # 主键ID（整数类型）
            # "id": 0,
            # 执行器主键ID（整数类型，关联执行器配置）
            "jobGroup": 1,
            # 任务描述信息（字符串类型）required
            "jobDesc": params["jobDesc"],  # "test_shell_" + generate_random_string(5),
            # 任务创建时间（日期类型，通常用字符串表示，如"2023-01-01 00:00:00"）
            "addTime": None,
            # 任务更新时间（日期类型，同上）
            "updateTime": None,
            # 任务负责人（字符串类型，通常为用户名）
            "author": params.get("author") or "admin",
            # 报警邮件（字符串类型，多个邮箱可用逗号分隔）
            "alarmEmail": params.get("alarmEmail") or "",
            # 调度类型（字符串类型，如"CRON"、"FIX_RATE"等）
            "scheduleType": params.get("scheduleType") or "CRON",  # CRON
            # 调度配置（字符串类型，值格式取决于调度类型，如CRON表达式） required
            "scheduleConf": params.get("scheduleConf"),  # 0/2 * * * * ?
            "cronGen_display": params.get("scheduleConf"),
            "schedule_conf_CRON": params.get("scheduleConf"),
            # 调度过期策略（字符串类型，如"DO_NOTHING"、"FIRE_ONCE_NOW"等）
            "misfireStrategy": params.get("misfireStrategy") or "DO_NOTHING",
            # 执行器路由策略（字符串类型，如"ROUND"、"RANDOM"等）
            "executorRouteStrategy": params.get("executorRouteStrategy") or "ROUND",
            # 执行器任务Handler名称（字符串类型，对应执行器中定义的处理类）
            "executorHandler": params.get("executorHandler") or "",
            # 执行器任务参数（字符串类型，传递给任务的参数）required
            "executorParam": params.get("executorParam"),  # 可空字符串 ""
            # 阻塞处理策略（字符串类型，如"DISCARD_LATER"、"SERIAL_EXECUTION"等）
            "executorBlockStrategy": params.get("executorBlockStrategy") or "DISCARD_LATER",
            # 任务执行超时时间（整数类型，单位：秒）
            "executorTimeout": params.get("executorTimeout") or 300,
            # 失败重试次数（整数类型，任务失败后重试的次数）
            "executorFailRetryCount": params.get("executorFailRetryCount") or 3,
            # GLUE类型（字符串类型，如"GLUE_SHELL"、"GLUE_PYTHON"等）required
            "glueType": params.get("glueType"),  # GLUE_PYTHON | GLUE_SHELL
            # GLUE源代码（字符串类型，存储脚本代码内容）required
            "glueSource": params.get("glueSource"),
            # "#!/bin/bash\n echo \"xxl-job: hello shell\"\n\n echo \"脚本位置：$0\"\n echo \"任务参数：$1\"\n echo \"分片序号 = $2\"\n echo \"分片总数 = $3\"\n\n echo \"Good bye!\"\n exit 0\n",
            # GLUE备注（字符串类型，对脚本的说明信息）
            "glueRemark": params.get("glueRemark") or "GLUE代码初始化",
            # GLUE更新时间（日期类型，脚本最后更新时间）
            "glueUpdatetime": None,
            # 子任务ID（字符串类型，多个子任务ID用逗号分隔）
            "childJobId": params.get("childJobId") or "",
            # 调度状态（整数类型，0-停止，1-运行）
            "triggerStatus": params.get("triggerStatus") or 0,
            # 上次调度时间（长整数类型，时间戳格式）
            "triggerLastTime": 0,
            # 下次调度时间（长整数类型，时间戳格式）
            "triggerNextTime": 0,
            # 忽略
            "schedule_conf_FIX_RATE": "",
            "schedule_conf_FIX_DELAY": "",
        }

        request_url = self.url + f"/xxl-job-admin/jobinfo/add"
        headers = self.headers

        resp = self.post(request_url, headers=headers, payload=payload)
        return build_resp(resp.get("code"), resp.get("msg"), {"id": resp.get("data")})

    # 任务信息
    def job_info(self, params: dict):
        request_url = self.url + f"/xxl-job-admin/jobinfo/info"
        headers = self.headers
        print(headers)
        payload = {
            "id": params.get("id"),
        }
        return self.post(request_url, headers=headers, payload=payload)

    # 删除任务
    def job_remove(self, id: int):
        request_url = self.url + f"/xxl-job-admin/jobinfo/remove"
        headers = self.headers

        payload = {
            "id": id,
        }

        return self.post(request_url, headers=headers, payload=payload)

    # 执行一次
    def job_run_once(self, params: dict):
        request_url = self.url + f"/xxl-job-admin/jobinfo/trigger"
        headers = self.headers
        payload = {
            "id": params.get("id"),
            "executorParam": params.get("executorParam"),
            "addressList": "",
        }
        return self.post(request_url, headers=headers, payload=payload)

    # 开始调度
    def job_start(self, params: dict):
        request_url = self.url + f"/xxl-job-admin/jobinfo/start"
        headers = self.headers
        payload = {
            "id": params.get("id"),
        }
        return self.post(request_url, headers=headers, payload=payload)

    # 停止调度
    def job_stop(self, params: dict):
        request_url = self.url + f"/xxl-job-admin/jobinfo/stop"
        headers = self.headers
        payload = {
            "id": params.get("id"),
        }
        return self.post(request_url, headers=headers, payload=payload)


def login():
    url = "http://localhost:8080"
    resp = XXLJob(url).login("admin", "123456")
    dump(resp)


def get_xxl_job() -> XXLJob:
    token = "eyJ1c2VySWQiOiIxIiwiZXhwaXJlVGltZSI6MCwic2lnbmF0dXJlIjoiZmU1YTk5MjlmYmIxNDAzZWE5YjYwMTgyODM0NmI2NzIifQ"
    # token = None
    xxl_job = XXLJob(url="http://localhost:8080", token=token)
    # login_resp = xxl_job.login("admin", "123456")
    # dump(login_resp)
    return xxl_job


def chart_info():
    xxl_job = get_xxl_job()
    resp = xxl_job.chart_info()
    dump(resp)


def job_add():
    xxl_job_info = {
        # 任务描述信息（字符串类型）
        "jobDesc": "test_python_" + generate_random_string(5),
        # 调度配置（字符串类型，值格式取决于调度类型，如CRON表达式）
        "scheduleConf": "0/2 * * * * ?",
        # 执行器任务参数（字符串类型，传递给任务的参数）
        "executorParam": "--run local",
        # 任务执行超时时间（整数类型，单位：秒）
        "executorTimeout": 300,
        # 失败重试次数（整数类型，任务失败后重试的次数）
        "executorFailRetryCount": 30,
        # GLUE类型（字符串类型，如"GLUE_SHELL"、"GLUE_PYTHON"等）GLUE_PYTHON | GLUE_SHELL
        "glueType": "GLUE_PYTHON",
        # GLUE源代码（字符串类型，存储脚本代码内容）
        "glueSource": "#!/bin/bash\n echo \"xxl-job: hello shell\"\n\n echo \"脚本位置：$0\"\n echo \"任务参数：$1\"\n echo \"分片序号 = $2\"\n echo \"分片总数 = $3\"\n\n echo \"Good bye!\"\n exit 0\n",
        # GLUE备注（字符串类型，对脚本的说明信息）
        "glueRemark": "GLUE代码初始化",
    }
    xxl_job = get_xxl_job()
    resp = xxl_job.job_add(xxl_job_info)
    dump(resp)


def job_remove():
    xxl_job = get_xxl_job()
    ids = [9, 10, 11, 13]
    for id in ids:
        resp = xxl_job.job_remove(id)
        dump(resp)


def job_run_once():
    xxl_job = get_xxl_job()
    params = {
        "id": 8,
        "executorParam": "--run local"
    }
    resp = xxl_job.job_run_once(params)
    dump(resp)


def job_start():
    xxl_job = get_xxl_job()
    params = {
        "id": 8,
    }
    resp = xxl_job.job_start(params)
    dump(resp)


def job_stop():
    xxl_job = get_xxl_job()
    params = {
        "id": 8,
    }
    resp = xxl_job.job_stop(params)
    dump(resp)


def job_info():
    xxl_job = get_xxl_job()
    params = {
        "id": 8,
    }
    resp = xxl_job.job_info(params)
    dump(resp)


if __name__ == '__main__':
    # job_remove()
    # job_stop()
    # job_add()
    # job_info()
    # job_start()
    # job_run_once()
    # chart_info()
    # login()
    # get_xxl_job()
    pass
