import builtins
import sys
import os
import requests
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging
import aiohttp
import asyncio

# 确保 'open' 函数在代码中可用
if not hasattr(builtins, 'open'):
    builtins.open = open

# 配置日志记录
logging.basicConfig(filename='errors.log', level=logging.ERROR, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

async def get_common_pattern(url):
    """ 从目标网站的首页提取常见的字符串或模式 """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    # 提取页面中的所有文本
                    text = soup.get_text()
                    # 这里可以添加更多的逻辑来提取特定的模式
                    return text[:10]  # 返回前10个字符作为示例
    except aiohttp.ClientError as e:
        logging.error(f"错误: {e} - {url}")
    except Exception as e:
        logging.error(f"未知错误: {e} - {url}")
    return ""

async def check_directory(session, url, directory, common_pattern):
    url = url.rstrip('/')
    full_url = f"{url}/{directory.strip()}"
    try:
        async with session.get(full_url, ssl=False) as response:
            if response.status == 200:
                text = await response.text()
                if common_pattern not in text:
                    return full_url
    except aiohttp.ClientError as e:
        logging.error(f"错误: {e} - {full_url}")
    except Exception as e:
        logging.error(f"未知错误: {e} - {full_url}")
    return None

async def run_blast(url, wordlist_path, threads):
    common_pattern = await get_common_pattern(url)
    with open(wordlist_path, 'r') as file:
        directories = file.readlines()
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=threads)) as session:
        tasks = [check_directory(session, url, directory, common_pattern) for directory in directories]
        results = []
        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="扫描进度"):
            try:
                result = await f
                if result:
                    tqdm.write(f"200: {result.strip()}")
                    results.append(result)
            except Exception as e:
                logging.error(f"任务执行错误: {e}")
    return results

def parse_arguments():
    parser = argparse.ArgumentParser(description="目录爆破工具")
    parser.add_argument("-u", "--url", required=True, help="目标 URL")
    parser.add_argument("-w", "--wordlist", nargs='?', default=DEFAULT_WORDLIST, help="字典文件路径")
    parser.add_argument("-t", "--threads", type=int, default=50, help="线程数")
    return parser.parse_args()

def main():
    print("--------------------------------------------------------------")
    print("|      _   _                  _       _                 _    |")
    print("|   __| | (_)  _ __          | |__   | |   __ _   ___  | |   |")
    print("|  / _` | | | | '__|  _____  | '_ \  | |  / _` | / __| | __| |")
    print("| | (_| | | | | |    |_____| | |_) | | | | (_| | \__ \ | |_  |")
    print("|  \__,_| |_| |_|            |_.__/  |_|  \__,_| |___/  \__| |")
    print("--------------------------------------------------------------")
    args = parse_arguments()
    asyncio.run(run_blast(args.url, resource_path(args.wordlist), args.threads))

if __name__ == "__main__":
    main()