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
from utils import load_wordlist, resource_path  # 导入 load_wordlist 和 resource_path 函数
from sqlscan.sqlscan import scan_sql_injection  # 导入 scan_sql_injection 函数

# 确保 'open' 函数在代码中可用
if not hasattr(builtins, 'open'):
    builtins.open = open

# 配置日志记录
logging.basicConfig(filename='errors.log', level=logging.ERROR, 
                    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s')

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

DEFAULT_WORDLIST = "file/dictionary.txt"
DEFAULT_PAYLOADS = "file/sqlscan.txt"

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

def load_urls_from_folder(folder_path):
    """ 从指定文件夹中读取所有 URL """
    urls = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                urls.extend([line.strip() for line in f.readlines()])
    return urls

async def run_blast(url, wordlist_path, threads, sql_scan):
    if not sql_scan:
        common_pattern = await get_common_pattern(url)
        directories = load_wordlist(wordlist_path)
        
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=threads)) as session:
            tasks = [check_directory(session, url, directory, common_pattern) for directory in directories]
            results = []
            for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="扫描进度"):
                try:
                    result = await f
                    if result:
                        tqdm.write(f"200: {result.strip()}")
                        results.append(result.strip())
                except Exception as e:
                    logging.error(f"任务执行错误: {e}")
        
        # 创建以扫描的 URL 命名的文件夹
        url_folder = url.replace("http://", "").replace("https://", "").replace("/", "_")
        if not os.path.exists(url_folder):
            os.makedirs(url_folder)
        
        # 将扫描结果保存到文件中
        results_file = os.path.join(url_folder, "results.txt")
        with open(results_file, 'w') as f:
            for result in results:
                f.write(result + "\n")
    else:
        if os.path.isdir(url):
            results = load_urls_from_folder(url)
        else:
            results = [url]
    
    # 如果启用了 SQL 扫描，则调用 scan_sql_injection 函数
    if sql_scan:
        payloads = load_wordlist(resource_path(DEFAULT_PAYLOADS))
        vulnerable_endpoints = scan_sql_injection(url, results, payloads)
        if vulnerable_endpoints:
            print("Vulnerable endpoints found:")
            for endpoint in vulnerable_endpoints:
                print(endpoint)
    
    return results

def parse_arguments():
    parser = argparse.ArgumentParser(description="目录爆破工具")
    parser.add_argument("-u", "--url", help="目标 URL 或包含 URL 的文件夹路径")
    parser.add_argument("-w", "--wordlist", nargs='?', default=DEFAULT_WORDLIST, help="字典文件路径")
    parser.add_argument("-t", "--threads", type=int, default=50, help="线程数")
    parser.add_argument("-s", "--sql", action='store_true', help="启用 SQL 扫描")
    args = parser.parse_args()
    
    # 检查是否提供了 URL 参数
    if not args.url:
        parser.print_help()
        parser.exit()
    
    return args

def main():
    print("--------------------------------------------------------------")
    print("|      _   _                  _       _                 _    |")
    print("|   __| | (_)  _ __          | |__   | |   __ _   ___  | |   |")
    print("|  / _` | | | '  __|  _____  | '_ \  | |  / _` | / __| | __| |")
    print("| | (_| | | | | |    |_____| | |_) | | | | (_| | \__ \ | |_  |")
    print("|  \__,_| |_| |_|            |_.__/  |_|  \__,_| |___/  \__| |")
    print("--------------------------------------------------------------")
    args = parse_arguments()
    asyncio.run(run_blast(args.url, resource_path(args.wordlist), args.threads, args.sql))

if __name__ == "__main__":
    main()