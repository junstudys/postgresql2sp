from pathlib import Path
import csv

def read_csv(file_path: str) -> list:
    """读取CSV文件内容"""
    with open(file_path, 'r', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

def read_file(file_path: str) -> list:
    """读取文件内容"""
    with open(file_path, 'r') as file:
        return file.readlines()
