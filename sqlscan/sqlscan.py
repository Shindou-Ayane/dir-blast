import requests
import argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import sys
import os

# 添加当前目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_wordlist, resource_path  # 导入 load_wordlist 和 resource_path 函数

def find_endpoints(url):
    """ 从目标网站的首页提取所有链接作为端点 """
    endpoints = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            parsed_url = urlparse(href)
            if parsed_url.netloc == '' or parsed_url.netloc == urlparse(url).netloc:
                endpoints.add(parsed_url.path)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return list(endpoints)

def scan_sql_injection(url, endpoints, payloads):
    vulnerable_endpoints = []

    for endpoint in endpoints:
        full_url = urljoin(url, endpoint)
        for payload in payloads:
            try:
                response = requests.get(full_url, params={"q": payload})
                if "syntax error" in response.text.lower() or "mysql" in response.text.lower():
                    print(f"Potential SQL Injection vulnerability found at {full_url} with payload {payload}")
                    vulnerable_endpoints.append(full_url)
                    break
            except requests.RequestException as e:
                print(f"Error scanning {full_url}: {e}")

    return vulnerable_endpoints

def parse_arguments():
    parser = argparse.ArgumentParser(description="SQL 注入扫描工具")
    parser.add_argument("-u", "--url", required=True, help="目标 URL")
    parser.add_argument("-p", "--payloads", default="file/sqlscan.txt", help="SQL 注入 payloads 文件路径")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    url = args.url
    endpoints = find_endpoints(url)
    payloads = load_wordlist(resource_path(args.payloads))
    vulnerable_endpoints = scan_sql_injection(url, endpoints, payloads)
    if vulnerable_endpoints:
        print("Vulnerable endpoints found:")
        for endpoint in vulnerable_endpoints:
            print(endpoint)
    else:
        print("No vulnerabilities found.")