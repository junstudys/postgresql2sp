def write_file(file_path: str, content: str) -> None:
    """写入文件内容"""
    with open(file_path, 'w') as file:
        file.write(content)
