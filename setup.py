from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('config_files', ['config_files/SP_Snippet_Begin.sql', 'config_files/正则替换参数.csv']),
    ('original_files', ['original_files/SQL_text.sql']),
    # 也可以包含空目录
    ('results', []),
    ('file_utils',['file_utils/writer.py','file_utils/reader.py']),
    ('sql_processors',['sql_processors/encapsulator.py','sql_processors/generator.py','sql_processors/replacer.py']),
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5','re','sys','os','csv','pathlib','datetime'],  # 根据你的项目需要添加其他依赖
    'plist': {
        'CFBundleName': 'YourAppName',
        'CFBundleDisplayName': 'YourAppName',
        'CFBundleGetInfoString': "Your application description",
        'CFBundleIdentifier': "com.yourdomain.yourappname",
        'CFBundleVersion': "0.1",
        'CFBundleShortVersionString': "0.1",
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
