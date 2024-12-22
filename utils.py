import os
import sys

def load_wordlist(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def resource_path(relative_path):
    """ 获取资源的绝对路径，适用于开发和 PyInstaller """
    try:
        # PyInstaller 创建一个临时文件夹，并将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)