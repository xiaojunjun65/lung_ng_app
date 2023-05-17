import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QMessageBox, QComboBox
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt
import pandas as pd
from  ai.app_main import LungDetectionUI
from adminwin import AdminWindow
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("登录")
        self.resize(400, 200)

        # 设置颜色样式
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 230, 255))
        self.setPalette(palette)

        # 添加黑色标题
        title_label = QLabel("肺炎诊断系统", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: black;")

        # 创建控件
        self.username_label = QLabel("用户名:")
        self.password_label = QLabel("密码:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("登录")
        self.register_button = QPushButton("注册")
        self.user_type_combobox = QComboBox()
        self.user_type_combobox.addItems(["用户", "管理员"])

        # 设置CSS样式
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #333333;
            }
            QLineEdit, QComboBox {
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
        layout.addWidget(title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.user_type_combobox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)
        layout.addStretch()  # 添加一个弹性空间，使布局居中显示
        self.setLayout(layout)

        # 绑定按钮点击事件
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_type = self.user_type_combobox.currentText()

        # 使用 pandas 读取 "db.xlsx" 文件
        try:
            df = pd.read_excel("db.xlsx")
            yh_column = df["用户名"]
            ps_column = df["密码"]
            usr_column = df["权限"]
            # 判断用户名是否存在
            if username in yh_column.values:

                # 获取对应用户名的密码
                correct_password = ps_column[yh_column[yh_column == username].index[0]]
                usr_corr = usr_column[yh_column[yh_column == username].index[0]]
                if str(password) == str(correct_password) and user_type ==usr_corr and user_type =="管理员":
                    QMessageBox.information(self, "登录结果", f"{user_type} {username} 登录成功")
                    self.LungDetectionUI = LungDetectionUI(username,mode=1)
                    self.LungDetectionUI.show()
                    self.hide()
                    return
                if str(password) == str(correct_password) and user_type ==usr_corr:
                    QMessageBox.information(self, "登录结果", f"{user_type} {username} 登录成功")
                    self.LungDetectionUI = LungDetectionUI(username,mode=2)
                    self.LungDetectionUI.show()
                    self.hide()
                    return
            QMessageBox.warning(self, "登录结果", "暂无用户")
        except Exception as e:
            QMessageBox.warning(self, "登录结果", f"登录失败：{str(e)}")

    def register(self):
        # 在这里编写注册逻辑
        from register import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
