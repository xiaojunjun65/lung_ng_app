import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QColor, QPalette
import openpyxl
import os.path
from login import  LoginWindow

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("注册")
        self.resize(400, 200)

        # 设置颜色样式
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 230, 255))
        self.setPalette(palette)

        # 创建控件
        self.username_label = QLabel("用户名:")
        self.password_label = QLabel("密码:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton("注册")

        # 设置CSS样式
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #333333;
            }
            QLineEdit {
                font-size: 14px;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: #FFFFFF;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addStretch()  # 添加一个弹性空间，使布局居中显示
        self.setLayout(layout)

        # 绑定按钮点击事件
        self.register_button.clicked.connect(self.register)

    import pandas as pd

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()


        # 检查密码是否为空
        if not password:
            QMessageBox.warning(self, "注册结果", "密码不能为空")
            return

        # 在这里编写注册逻辑
        data = {'用户名': [username], '密码': [password]}
        df = pd.DataFrame(data)

        try:
            original_data = pd.read_excel('db.xlsx')
            save_data = original_data.append(df)

            save_data.to_excel('db.xlsx', index=False)

            QMessageBox.information(self, "注册结果", "注册成功")
            self.LoginWindow = LoginWindow()
            self.LoginWindow.show()
            self.hide()
        except Exception as e:
            QMessageBox.warning(self, "注册结果", f"注册失败：{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())
