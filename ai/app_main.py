import sys

import cv2
from PyQt5.QtCore import Qt
from ai.models.experimental import attempt_load
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox
import sys
from ai.detect import UI
from PIL import Image
from PIL.ImageQt import  ImageQt
from PyQt5.QtWidgets import *
from app.adminwin import AdminWindow
# #model_load
model = attempt_load(r'best.pt',map_location='cpu')
stride = int(model.stride.max())

class LungDetectionUI(QWidget):
    def __init__(self,username,mode=1):
        super().__init__()
        self.tupian = None
        # 设置窗口大小和标题
        self.setFixedSize(1280, 720)
        self.setWindowTitle("肺炎诊断系统")
        self.username = username
        # 原图区域
        self.mode = mode
        self.original_image_label = QLabel()
        self.original_image_label.setFixedSize(380, 380)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("border: 1px solid black;")

        # 结果显示区域
        self.result_image_label = QLabel()
        self.result_image_label.setFixedSize(380, 380)
        self.result_image_label.setAlignment(Qt.AlignCenter)
        self.result_image_label.setStyleSheet("border: 1px solid black;")

        # 日志显示区域
        # self.log_label = QLabel("AI病例报告")
        # self.log_label.setFixedWidth(280)
        # self.log_label.setStyleSheet("border: 1px solid black;")

        # AI病例报告
        self.report_label = QLabel("AI病例报告")
        self.report_label.setStyleSheet("border: 1px solid black; font-size: 13px;")
        # 开始检测按钮
        self.start_button = QPushButton("开始检测")
        self.start_button.setFixedSize(100, 30)
        self.select = QPushButton("选择图片")
        self.select.setFixedSize(100, 30)
        self.select.clicked.connect(self.xianshi)
        # 布局
        layout = QHBoxLayout()

        layout.addWidget(self.original_image_label)

        layout.addWidget(self.result_image_label)

        layout.addWidget(self.report_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select)
        button_layout.addWidget(self.start_button)
        button_layout.setContentsMargins(0, 0, 0, 30)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        #clie
        if self.mode==1:
            self.houtai = QPushButton("后台管理")
            self.houtai.setFixedSize(100, 30)
            self.houtai.clicked.connect(self.hhh)
            button_layout.addWidget(self.houtai)

        self.start_button.clicked.connect(self.AI)
    def AI(self):

        cls = []
        conf = []
        guji = []
        zhengchang = 0
        yichang =0
        img,conf,cls = UI(self.tupian,model,stride)

        ai_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ai_img = ImageQt(ai_img)
        from PyQt5 import QtGui
        ai_img = QtGui.QPixmap.fromImage(ai_img).scaled(self.result_image_label.width(),
                                                      self.result_image_label.height())
        self.result_image_label.setPixmap((ai_img))
        for i in range(len(cls)):
            if cls[i] ==0:
                zhengchang+=1
            else:
                yichang+=1
                guji.append(conf[i])
        if zhengchang ==2:
            rizhi ="肺部处于正常状态"
        if len(guji)==1:
            zhi = max(guji)
            if zhi <40:
                rizhi='肺部处于异常状态，有小部分透析缺失，初期'
            if zhi <60 and zhi>40:
                rizhi='肺部处于异常状态，与正常比对有透明缺失状，中期'
            if zhi >60:
                rizhi='肺部处于严重异常状态，肺部呈完全或半透明，肺' \
                      '部阴影成像不全，晚期'
        if len(guji)==2:
                rizhi='双肺处于严重异常状态'
        str_log = '''
        =============================
        AI检测日志报告
        
        当前异常项：{}
        
        
        正常项：{}
        
        
        异常估计值：{}
        
        
        分析：{}。
        
        
        ==============================
        '''.format(yichang,zhengchang,guji,rizhi)
        self.report_label.setText(str_log)
    def hhh(self):
        self.AdminWindow = AdminWindow(self.username)
        self.AdminWindow.show()
        self.hide()
    def xianshi(self):
        imgname, imgtype = QFileDialog.getOpenFileName(None, "选择图片", " ")
        yuantu = cv2.imread(imgname)
        img = Image.fromarray(cv2.cvtColor(yuantu, cv2.COLOR_BGR2RGB))
        qimg = ImageQt(img)
        from PyQt5 import QtGui
        pixmax = QtGui.QPixmap.fromImage(qimg).scaled(self.original_image_label.width(),
                                                      self.original_image_label.height())
        self.original_image_label.setPixmap((pixmax))
        self.tupian=yuantu


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LungDetectionUI(username="aaa")
    window.show()
    sys.exit(app.exec_())
