import requests
from concurrent.futures import ThreadPoolExecutor
import argparse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def check_directory(url, directory):
    url = url.rstrip('/')
    full_url = f"{url}/{directory.strip()}"
    try:
        response = requests.get(full_url, verify=False)  # 忽略 SSL 证书验证
        if response.status_code == 200:
            print(f"200: {full_url}")
        elif response.status_code == 201:  
            print(f"201: {full_url}")
        elif response.status_code == 202:
            print(f"202: {full_url}")
        elif response.status_code == 203:
            print(f"203: {full_url}")
        elif response.status_code == 204:
            print(f"204: {full_url}")
        elif response.status_code == 205:
            print(f"205: {full_url}")
        elif response.status_code == 206:
            print(f"206: {full_url}")
        elif response.status_code == 405:
            print(f"405: {full_url}")
        elif response.status_code == 403:
            print(f"403: {full_url}")
        elif response.status_code == 401:
            print(f"401: {full_url}")
        elif response.status_code == 307:
            print(f"307: {full_url}")
    except requests.RequestException as e:
        print(f"Error: {e} - {full_url}")

def load_wordlist(wordlist_path):
    with open(wordlist_path, 'r') as f:
        return f.readlines()

def parse_arguments():
    parser = argparse.ArgumentParser(description="目录暴力破解工具")
    parser.add_argument('-u', '--url', required=True, help='目标 URL 地址')
    parser.add_argument('-w', '--wordlist', default='file/dictionary.txt', help='字典文件路径（默认: file/dictionary.txt）')
    parser.add_argument('-t', '--threads', type=int, default=20, help='线程数（默认: 20）')
    return parser.parse_args()

def run_blast(url, wordlist, threads):
    directories = load_wordlist(wordlist)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for directory in directories:
            executor.submit(check_directory, url, directory)