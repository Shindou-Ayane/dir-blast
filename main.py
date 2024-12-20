import requests
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def check_directory(url, directory):
    full_url = f"{url}/{directory.strip()}"
    try:
        response = requests.get(full_url, verify=False)
        if response.status_code == 200:
            print(f"200: {full_url}")
        if response.status_code == 201:  
            print(f"201: {full_url}")
        if response.status_code == 202:
            print(f"202: {full_url}")
        if response.status_code == 203:
            print(f"203: {full_url}")
        if response.status_code == 204:
            print(f"204: {full_url}")
        if response.status_code == 205:
            print(f"205: {full_url}")
        if response.status_code == 206:
            print(f"206: {full_url}")
        if response.status_code == 405:
            print(f"405: {full_url}")
        if response.status_code == 403:
            print(f"403: {full_url}")
        if response.status_code == 401:
            print(f"401: {full_url}")
        if response.status_code == 307:
            print(f"307: {full_url}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {full_url} - {e}")

def dir_bruteforce(url, wordlist):
    with open(wordlist, 'r') as file:
        directories = file.readlines()
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(lambda directory: check_directory(url, directory), directories)

if __name__ == "__main__":
    print("--------------------------------------------------------------")
    print("|      _   _                  _       _                 _    |")
    print("|   __| | (_)  _ __          | |__   | |   __ _   ___  | |   |")
    print("|  / _` | | | | '__|  _____  | '_ \  | |  / _` | / __| | __| |")
    print("| | (_| | | | | |    |_____| | |_) | | | | (_| | \__ \ | |_  |")
    print("|  \__,_| |_| |_|            |_.__/  |_|  \__,_| |___/  \__| |")
    print("--------------------------------------------------------------")
    print("")
    url = input("Enter the target URL: ")
    if url[-1] == "/":
        url = url[:-1]
    wordlist_path = "./file/dictionary.txt"
    dir_bruteforce(url, wordlist_path)