"""
auther:linklinco@github
time:2025-04-05
version:0.1
"""

import sys
import requests
import json
import re
import uuid
import os
from urllib.parse import urlparse

"""
使用前，请先配置好这三个全局变量

url 为部署兰空图床的域名
email 为兰空图床的邮箱
password 为兰空图床设置的密码
"""


url = ""
email = ""
password = ""


def isRemoteUrl(uri):
    """判断是否为有效的远程URL（支持http/https/ftp/scp/sftp）"""
    url_pattern = re.compile(
        r'^(https?|ftp|scp|sftp)://'  # 协议
        # 域名
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # 本地主机
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IPv4地址
        r'(?::\d+)?'  # 端口
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return bool(url_pattern.match(uri))


def getToken():
    global url, username, password
    payload = json.dumps({
        "email": email,
        "password": password
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url+"/api/v1/tokens", headers=headers, data=payload)
    data = response.json()
    return data["data"]["token"]


def get_file_extension(url):
    response = requests.get(url, stream=True)

    # 方法1：Content-Disposition
    if "Content-Disposition" in response.headers:
        _, params = response.headers["Content-Disposition"].split(";")
        filename = params.replace("filename=", "").strip('"')
        return os.path.splitext(filename)[1]

    # 方法2：URL路径
    path = urlparse(url).path
    if "." in path:
        return os.path.splitext(path)[1]

    # 方法3：Content-Type
    content_type = response.headers.get("Content-Type", "")
    if "image/jpeg" in content_type:
        return ".jpg"
    elif "application/zip" in content_type:
        return ".zip"

    return ".png"  # 无法确定后缀


def saveImage(url):
    user_home = os.path.expanduser("~")
    image_path = os.path.join(user_home, "images")
    os.makedirs(image_path, exist_ok=True)
    response = requests.get(url, stream=True)
    file_name = uuid.uuid4().hex[:16]+get_file_extension(url)

    output_path = os.path.join(image_path, file_name)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path


def upload(filePath: str):
    global url, token
    if isRemoteUrl(filePath):
        filePath = saveImage(filePath)

    payload = {}
    files = [
        ('file', (filePath, open(filePath, 'rb'), 'image/jpeg'))
    ]
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        # 'Content-Type': 'multipart/form-data',

    }
    response = requests.request(
        "POST", url+"/api/v1/upload", headers=headers, data=payload, files=files)
    data = response.json()
    return data["data"]["links"]["url"]


if __name__ == "__main__":
    # 第一个参数是脚本名，后续为传入的参数

    global token
    token = getToken()
    if len(sys.argv) < 2:
        print("error:need two argvs")
        sys.exit(1)
    else:
        # print(upload(sys.argv[1]))
        for i in range(1, len(sys.argv)):
            print(upload(sys.argv[i]))
        sys.exit(0)
