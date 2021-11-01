from UI.WeChatOCR import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QCheckBox
import tools.infer.predict_system as predict_system
import tools.infer.utility as utility
import excel.excel as excel
import os

info = {
    '收款人': [],
    '金额': [],
    '当前状态': [],
    '商品': [],
    '商户全称': [],
    '支付时间': [],
    '支付方式': [],
    '交易单号': [],
    '商户单号': []
}
def transfer(single_result):
    i = 0;
    while i < len(single_result):
        if single_result[i] == '当前状态':
            info['收款人'].append(single_result[i - 2])
            info['金额'].append(str(abs(float(single_result[i - 1]))))
            for key in info:
                if key not in ['收款人', '金额']:
                    allKeys = info.keys()
                    j = i + 1
                    s = single_result[j]
                    j += 1
                    finish = False;
                    while single_result[j] not in allKeys:
                        if key == '商户单号':
                            finish = True
                            if '扫码' in s:
                                s = ''
                        s += single_result[j]
                        j += 1
                        if '群收款' in single_result[j]:
                            break
                    info[key].append(s)
                    i = j
                    if finish:
                        return
        else:
            i += 1

class MyMainWindow(QMainWindow, Ui_MainWindow):
    img_path = ""
    dist_path = ""
    checkbox_list = []
    info_dict = {}
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.img_path_pushButton.clicked.connect(self.setImgPath)
        self.excel_path_pushButton.clicked.connect(self.setExcelPath)
        self.pushButton.clicked.connect(self.operator)
        self.checkbox_list = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4,self.checkBox_5,
                              self.checkBox_6, self.checkBox_7, self.checkBox_8, self.checkBox_9, self.checkBox_10]
        self.progressBar.setValue(0)

    def setImgPath(self):
        self.img_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                   "浏览",
                                                                   "C:")
        self.img_path_lineEdit.setText(self.img_path)

    def setExcelPath(self):
        self.dist_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                   "浏览",
                                                                   "C:")
        self.excel_path_lineEdit.setText(self.dist_path)

    def select(self):
        for checkbox in self.checkbox_list:
            if checkbox.isChecked():
                key = checkbox.text()
                self.info_dict[key] = info[key]

    def progress(self, n, total):
        percent = ((n / total) * 100)
        self.progressBar.setValue(percent)

    def operator(self):
        filelist = os.listdir(self.img_path)
        i = 1
        for filename in filelist:
            result = predict_system.main(utility.parse_args(self.img_path + '/' + filename))
            transfer(result)
            self.progress(i, len(filelist))
            i += 1
        self.select()
        excel.To_Excel(self.info_dict, self.dist_path)
