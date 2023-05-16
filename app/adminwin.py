import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTableView
from PyQt5.QtGui import QFont, QColor, QPalette, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import pandas as pd

class AdminWindow(QWidget):
    def __init__(self, username):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle(f"管理员 {username} 你好")

        # 设置窗口大小
        self.resize(1280, 720)

        # 设置背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 230, 255))
        self.setPalette(palette)

        # 创建布局
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        try:
            # 使用 pandas 读取 "db.xlsx" 文件
            df = pd.read_excel("db.xlsx")

            # 创建表格模型
            model = QStandardItemModel(df.shape[0], df.shape[1])
            model.setHorizontalHeaderLabels(df.columns)

            # 填充表格模型数据
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QStandardItem(str(df.iloc[row, col]))
                    model.setItem(row, col, item)

            # 创建表格视图并设置模型和样式
            table_view = QTableView()
            table_view.setModel(model)
            table_view.setShowGrid(True)
            table_view.horizontalHeader().setStyleSheet("border: 1px solid gray;")
            table_view.verticalHeader().setStyleSheet("border: 1px solid gray;")

            # 设置表格大小
            table_view.resize(1000, 600)

            layout.addWidget(table_view)
        except Exception as e:
            layout.addWidget(QLabel(f"读取内容失败：{str(e)}"))

        # 设置布局
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 假设当前登录的用户为 admin
    username = "admin"

    window = AdminWindow(username)
    window.show()

    sys.exit(app.exec_())
