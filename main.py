import sys
import os
import requests
from concurrent.futures import ThreadPoolExecutor
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

DEFAULT_WORDLIST = "file/dictionary.txt"

def resource_path(relative_path):
    """ 获取资源的绝对路径，适用于开发和 PyInstaller """
    try:
        # PyInstaller 创建一个临时文件夹，并将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_common_pattern(url):
    """ 从目标网站的首页提取常见的字符串或模式 """
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取页面中的所有文本
            text = soup.get_text()
            # 这里可以添加更多的逻辑来提取特定的模式
            return text[:20]  # 返回前20个字符作为示例
    except requests.RequestException as e:
        print(f"错误: {e} - {url}")
    return ""

def check_directory(url, directory, common_pattern):
    url = url.rstrip('/')
    full_url = f"{url}/{directory.strip()}"
    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        response = session.get(full_url, verify=False, timeout=10)  # 忽略 SSL 证书验证，设置超时为10秒
        if response.status_code == 200:
            if common_pattern not in response.text:  # 使用提取的模式
                print(f"200: {full_url}")
                return full_url
    except requests.RequestException as e:
        print(f"错误: {e} - {full_url}")
    return None

def parse_arguments():
    parser = argparse.ArgumentParser(description="目录暴破工具")
    parser.add_argument("-u", "--url", required=True, help="目标 URL")
    parser.add_argument("-w", "--wordlist", nargs='?', default=DEFAULT_WORDLIST, help="字典文件路径")
    parser.add_argument("-t", "--threads", type=int, default=20, help="线程数")
    return parser.parse_args()

def run_blast(url, wordlist_path, threads):

    common_pattern = get_common_pattern(url)
    with open(wordlist_path, 'r') as file:
        directories = file.readlines()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for directory in tqdm(executor.map(lambda directory: check_directory(url, directory, common_pattern), directories), total=len(directories), desc="扫描进度"):
            if directory:
                tqdm.write(f"200: {directory.strip()}")

def main():
    print("--------------------------------------------------------------")
    print("|      _   _                  _       _                 _    |")
    print("|   __| | (_)  _ __          | |__   | |   __ _   ___  | |   |")
    print("|  / _` | | | | '__|  _____  | '_ \  | |  / _` | / __| | __| |")
    print("| | (_| | | | | |    |_____| | |_) | | | | (_| | \__ \ | |_  |")
    print("|  \__,_| |_| |_|            |_.__/  |_|  \__,_| |___/  \__| |")
    print("--------------------------------------------------------------")
    args = parse_arguments()
    run_blast(args.url, resource_path(args.wordlist), args.threads)

if __name__ == "__main__":
    main()