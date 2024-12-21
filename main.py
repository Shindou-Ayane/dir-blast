import sys
import os
import requests
from concurrent.futures import ThreadPoolExecutor
import argparse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

DEFAULT_WORDLIST = "file/dictionary.txt"  # 默认字典文件路径

def resource_path(relative_path):
    """ 获取资源的绝对路径，适用于开发和 PyInstaller """
    try:
        # PyInstaller 创建一个临时文件夹，并将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
    except requests.RequestException as e:
        print(f"错误: {e} - {full_url}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="目录暴力破解工具")
    parser.add_argument("-u", "--url", help="目标 URL")
    parser.add_argument("-w", "--wordlist", nargs='?', default=DEFAULT_WORDLIST, help="字典文件路径（默认: default_wordlist.txt）")
    parser.add_argument("-t", "--threads", type=int, default=10, help="线程数")
    return parser.parse_args()

def run_blast(url, wordlist_path, threads):
    with open(wordlist_path, 'r') as file:
        directories = file.readlines()
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for directory in directories:
            executor.submit(check_directory, url, directory)

def main():
    print("--------------------------------------------------------------")
    print("|      _   _                  _       _                 _    |")
    print("|   __| | (_)  _ __          | |__   | |   __ _   ___  | |   |")
    print("|  / _` | | | | '__|  _____  | '_ \  | |  / _` | / __| | __| |")
    print("| | (_| | | | | |    |_____| | |_) | | | | (_| | \__ \ | |_  |")
    print("|  \__,_| |_| |_|            |_.__/  |_|  \__,_| |___/  \__| |")
    print("--------------------------------------------------------------")
    
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    
    args = parse_arguments()
    run_blast(args.url, resource_path(args.wordlist), args.threads)

if __name__ == "__main__":
    main()