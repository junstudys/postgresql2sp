import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox

import datetime
from pathlib import Path
#from configparser import ConfigParser
from file_utils.reader import read_csv, read_file
from file_utils.writer import write_file
from sql_processors.replacer import replace_content
from sql_processors.encapsulator import encapsulate_sql
from sql_processors.generator import generate_sp

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 获取main.py所在的目录
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # 使用os.path.join和base_dir确保跨平台兼容性
        self.default_regex_path = os.path.join(self.base_dir, 'config_files', '正则替换参数.csv')
        self.default_sql_template_path = os.path.join(self.base_dir, 'config_files', 'SP_Snippet_Begin.sql')
        # 默认结果输出路径
        self.default_output_path = os.path.join(self.base_dir, 'results')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PostgreSQL转存储过程')
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        # 创建输入框但不显示默认路径
        self.originalSqlLabel = QLabel("原始SQL文件路径:")
        self.originalSqlPath = QLineEdit()
        self.spNameLabel = QLabel("存储过程名称:")
        self.spName = QLineEdit()
        self.remarkLabel = QLabel("存储过程备注(选填):")
        self.remark = QLineEdit()
        self.outputPathLabel = QLabel("结果文件夹:")
        self.outputPath = QLineEdit(self.default_output_path)  # 设置默认结果输出路径


        # 浏览按钮
        self.originalSqlBrowseButton = QPushButton('浏览')
        self.outputPathBrowseButton = QPushButton('浏览')
        self.processButton = QPushButton('运行')

        # 设置布局
        layout.addWidget(self.originalSqlLabel)
        layout.addWidget(self.originalSqlPath)
        layout.addWidget(self.originalSqlBrowseButton)
        layout.addWidget(self.outputPathLabel)
        layout.addWidget(self.outputPath)
        layout.addWidget(self.outputPathBrowseButton)
        layout.addWidget(self.spNameLabel)
        layout.addWidget(self.spName)
        layout.addWidget(self.remarkLabel)
        layout.addWidget(self.remark)
        layout.addWidget(self.processButton)

        self.originalSqlBrowseButton.clicked.connect(lambda: self.browseFile(self.originalSqlPath))
        self.outputPathBrowseButton.clicked.connect(lambda: self.browseFolder(self.outputPath))
        self.processButton.clicked.connect(self.processData)

        self.setLayout(layout)

    def browseFile(self, pathField):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.base_dir)
        if fname[0]:
            pathField.setText(fname[0])

    def browseFolder(self, pathField):
        dir = QFileDialog.getExistingDirectory(self, "Select Directory", self.base_dir)
        if dir:
            pathField.setText(dir)
    def processData(self):
        try:
            # 使用默认路径和用户输入执行处理逻辑
            regex_file = self.default_regex_path
            sql_template = self.default_sql_template_path
            original_sql = self.originalSqlPath.text()
            sp_name = self.spName.text()
            remark = self.remark.text()
            output_path = self.outputPath.text()

            print(f"正在处理数据... 使用配置：{regex_file}, {sql_template}, {original_sql}, {sp_name}, {remark}")
            # 添加实际的数据处理逻辑
            regex_params = read_csv(regex_file)
            original_sql_content = read_file(original_sql)
            replaced_sql_content = replace_content(original_sql_content, regex_params)
            encapsulated_sql_content = encapsulate_sql(replaced_sql_content)
            final_sp = generate_sp(encapsulated_sql_content, sql_template, sp_name, remark, datetime.date.today())
            write_file(f'{output_path}/SP_{sp_name}.sql', final_sp)

            # 模拟处理逻辑
            if not os.path.exists(regex_file) or not os.path.exists(sql_template) or not os.path.exists(original_sql):
                raise FileNotFoundError("一个或多个文件未找到，请检查路径是否正确。")

            # 显示成功消息
            QMessageBox.information(self, "成功", "处理完成。", QMessageBox.Ok)

        except Exception as e:
            # 显示错误消息
            QMessageBox.critical(self, "错误", str(e), QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppWindow()
    ex.show()
    sys.exit(app.exec_())
