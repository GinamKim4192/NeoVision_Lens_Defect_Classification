from cProfile import label
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
import os
import numpy as np
import shutil
from tqdm import tqdm

DEFAULT_PROGRESS_STYLE="""
#move_progress {
    text-align : center;
    height : 15px;
}
#move_progress::chunk {
    background-color : orange;
    width: 10px;
    margin: 0.5px;
}
"""

# table_color ="""
# QTableWidget::item{ selection-background-color: red}
# """


formclass = uic.loadUiType('lenslabel.ui')[0]
class WindowClass(QMainWindow, formclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move_progress.setStyleSheet(DEFAULT_PROGRESS_STYLE)

        self.label_name.setColumnCount(2)
        self.label_name.setHorizontalHeaderLabels(['Label', 'Count'])
        self.label_name.setRowCount(7)
        self.label_name.setItem(0, 0, QTableWidgetItem('1_normal'))
        self.label_name.setItem(1, 0, QTableWidgetItem('2_center'))
        self.label_name.setItem(2, 0, QTableWidgetItem('3_colorpoor'))
        self.label_name.setItem(3, 0, QTableWidgetItem('4_dotmissing'))
        self.label_name.setItem(4, 0, QTableWidgetItem('5_inkcut'))
        self.label_name.setItem(5, 0, QTableWidgetItem('6_line'))
        self.label_name.setItem(6, 0, QTableWidgetItem('7_etc'))
        self.label_name.setItem(0, 1, QTableWidgetItem('0'))
        self.label_name.setItem(1, 1, QTableWidgetItem('0'))
        self.label_name.setItem(2, 1, QTableWidgetItem('0'))
        self.label_name.setItem(3, 1, QTableWidgetItem('0'))
        self.label_name.setItem(4, 1, QTableWidgetItem('0'))
        self.label_name.setItem(5, 1, QTableWidgetItem('0'))
        self.label_name.setItem(6, 1, QTableWidgetItem('0'))


        self.dir_list.setColumnCount(2)
        self.dir_list.setHorizontalHeaderLabels(['File name', 'Label'])
        self.current_dir = ''

        self.add_label_name.setPlaceholderText('input label name')
        self.item_list = ['1_normal', '2_center', '3_colorpoor', '4_dotmissing', '5_inkcut', '6_line', '7_etc']

        self.dir_select.clicked.connect(self.select_dir)
        self.add_label.clicked.connect(self.add_label_btn)
        self.label_name.doubleClicked.connect(self.labeling_click)
        self.label_name.doubleClicked.connect(self.show_image)
        self.label_name.doubleClicked.connect(self.counting)
        self.dir_list.clicked.connect(self.show_image)
        self.dir_list.clicked.connect(self.repair_key_event)
        self.movefile.clicked.connect(self.file_move)
        self.subtraction_label.clicked.connect(self.subtraction_label_btn)
        self.repair_keyevent.clicked.connect(self.repair_key_event)


    # 더블클릭으로 라벨링
    def labeling_click(self):
        try:
            text = self.label_name.item(self.label_name.currentRow(), 0).text()
        except:
            return 0
        try:
            self.dir_list.setItem(self.dir_list.currentRow(), 1, QTableWidgetItem(text))
        except:
            QMessageBox.warning(self, 'Not Exist File', '파일이 존재하지 않음')
            return 0
        self.dir_list.setCurrentCell(self.dir_list.currentRow()+1, 0)
        if not self.file_count_3:
            QMessageBox.infomation(self, "EndLabeling", "끝")


    # 키보드로 라벨링, 이전 이미지 다음 이미지
    def keyPressNum(self, e):
        press_key_num = int(e.text())
        # 0번은 10번으로 바꿈
        if press_key_num == 0:
            press_key_num = 10
        else:
            press_key_num = press_key_num
        # Label 테이블의 2열 카운팅
        if self.label_name.rowCount() >= press_key_num and self.dir_list.rowCount():
            self.label_name.setCurrentCell(press_key_num - 1, 0)
            current_row = self.dir_list.currentRow()
            current_value = self.dir_list.item(current_row, 1)
            label_current_row = self.label_name.currentRow()
            label_current_value = self.label_name.item(label_current_row, 0)
            label_current_text = label_current_value.text() if label_current_value else ''
            current_text = current_value.text() if current_value else ''
            if not current_value:
                label_current_row = self.label_name.currentRow()
                label_current_value = int(self.label_name.item(label_current_row, 1). text())
                self.label_name.setItem(label_current_row, 1, QTableWidgetItem(str(label_current_value + 1)))
            elif label_current_text == current_text:
                pass
            else:
                label_current_row = self.label_name.currentRow()
                labeling_row = self.dir_list.currentRow()
                try:
                    current_label_row = self.label_name.currentRow()
                    current_label_value = int(self.label_name.item(current_label_row, 1). text())
                    previous_label = self.dir_list.item(labeling_row, 1).text()
                    previous_label_idx = self.item_list.index(previous_label)
                    previous_label_count = int(self.label_name.item(previous_label_idx, 1).text())
                except:
                    return 0
                self.label_name.setItem(previous_label_idx, 1, QTableWidgetItem(str(previous_label_count - 1)))
                self.label_name.setItem(label_current_row, 1, QTableWidgetItem(str(current_label_value + 1)))
                # self.label_name.setItem(previous_label_idx, 1, QTableWidgetItem(str(label_current_value - 1)))


        else:
            QMessageBox.warning(self, 'Not Exist File', '폴더를 불러오지 않거나 라벨 없음')
        self.labeling_click()
        self.show_image()
        self.counting()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_1:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_2:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_3:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_4:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_5:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_6:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_7:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_8:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_9:
            self.keyPressNum(e)
        elif e.key() == Qt.Key_0:
            self.keyPressNum(e)

        elif e.key() == Qt.Key_A:
            current_row = self.dir_list.currentRow()
            self.dir_list.setCurrentCell(current_row-1, 0)
            self.show_image()
        elif e.key() == Qt.Key_Minus:
            current_row = self.dir_list.currentRow()
            self.dir_list.setCurrentCell(current_row-1, 0)
            self.show_image()

        elif e.key() == Qt.Key_D:
            current_row = self.dir_list.currentRow()
            self.dir_list.setCurrentCell(current_row+1, 0)
            self.show_image()
        elif e.key() == Qt.Key_Plus:
            current_row = self.dir_list.currentRow()
            self.dir_list.setCurrentCell(current_row+1, 0)
            self.show_image()
        elif e.key() == Qt.Key_P:
            self.file_move()
            

    # 라벨 추가하기
    def add_label_btn(self):
        label_name = self.add_label_name.toPlainText()
        if not label_name:
            QMessageBox.warning(self, 'Emptied Label', '라벨명이 비어있음')
        elif len(self.item_list) and any(np.array(self.item_list) == label_name):
            QMessageBox.warning(self, 'Exist', '해당 이름의 라벨이 존재함')
        else:
            last_row = self.label_name.rowCount()
            print(last_row)
            current_row = self.label_name.currentRow()
            self.label_name.setRowCount(last_row+1)
            self.label_name.setItem(last_row, 0, QTableWidgetItem(label_name))
            self.label_name.setRowHeight(last_row, 40)
            self.add_label_name.clear()
            self.item_list.append(label_name)
            self.label_name.setItem(last_row, 1, QTableWidgetItem('0'))
            if last_row % 2 == 1:
                self.label_name.item(last_row, 0).setBackground(QtGui.QColor(255, 255, 200))
            else:
                self.label_name.item(last_row, 0).setBackground(QtGui.QColor(200, 200, 150))
        

    # 라벨 삭제하기
    def subtraction_label_btn(self):
        try:
            current_row = self.label_name.currentRow()
            current_name = self.label_name.item(current_row, 0).text()
            self.item_list.remove(current_name)
            self.label_name.removeRow(current_row)
            print(self.item_list)
        except:
            QMessageBox.warning(self, 'Not select label', '선택된 라벨이 없음')
            return 0
            

    # 이미지 출력
    def show_image(self):
        row = self.dir_list.currentRow()
        try:
            image_name = self.dir_list.item(row, 0).text()
        except:
            return 0
        image = QtGui.QPixmap(f'{self.current_dir}/{image_name}')
        image_resize = image.scaled(900, 900, Qt.KeepAspectRatio)
        self.imagebox.setPixmap(image_resize)
        self.repair_key_event


    # 라벨링 된 것과 안된것 갯수 세기
    def counting(self):
        label_row = self.label_name.currentRow()
        label_count = self.label_name.item(label_row, 1)
        dirlist_row = self.dir_list.currentRow()
        dirlist_value = self.dir_list.item(dirlist_row, 1)
        dirlist_text = dirlist_value.text() if dirlist_value else ''
        current_labeled_count = self.file_count_2.text()
        current_nolabeled_count = self.file_count_3.text()
        try:
            if not dirlist_text:
                self.file_count_2.setText(str(int(current_labeled_count) + 1))
                self.file_count_3.setText(str(int(current_nolabeled_count) - 1))
                self.label_name.setItem(label_row, 1, QTableWidgetItem(str(int(label_count) + int(1))))
        except:
            return 0


    # 디렉토리 열기
    def select_dir(self):
        # dir_path = QFileDialog.getExistingDirectory(self, 'select directory', filter='*.jpg')
        selected_dir = QFileDialog.getExistingDirectory(self, 'select directory')
        if selected_dir != '':
            self.current_dir = selected_dir
            dir_list = os.listdir(self.current_dir)
            self.label_name.setCurrentCell(0, 0)
            self.dir_list.setRowCount(0)
            self.dir_list.setRowCount(len(os.listdir(self.current_dir)))
            self.file_count.setText(str(len(os.listdir(self.current_dir))))
            self.file_count_2.setText(str(0))
            self.file_count_3.setText(str(len(os.listdir(self.current_dir))))
            self.dir_list.setCurrentCell(0, 0)
        else:
            return 0
        
        for idx, name in enumerate(dir_list):
            self.dir_list.setItem(idx, 0, QTableWidgetItem(name))
            self.dir_list.setRowHeight(idx, 20)
        self.show_image()
    

    # 라벨링 된 것 각각의 폴더로 이동
    def file_move(self):
        self.move_progress.setValue(0)
        progress_count = 0
        try:
            labeled_count = int(self.file_count_2.text())
        except:
            self.move_progress.setValue(100)
            return 0
        for dir in self.item_list:
            try:
                os.mkdir(f'./{dir}')
            except:
                continue
        for row in range(labeled_count):
            try:
                filename = self.dir_list.item(0, 0).text()
                label = self.dir_list.item(0, 1).text()
                shutil.move(f'{self.current_dir}/{filename}', f'{label}/{filename}')
            except:
                QMessageBox.warning(self, 'Can\'t make directiory', '1. 현재 첫번째 행이 빈값임. \n2. 혹시나 위의 Label을 지웠다면 해당 폴더를 만들지 못해 오류가 발생한 것으로 보임, 해당 라벨 다시 생성 필요')
                return 0
            self.dir_list.removeRow(0)
            current_labeled_num = self.file_count_2.text()
            current_filecount_num = self.file_count.text()
            self.file_count_2.setText(str(int(current_labeled_num) - 1))
            self.file_count.setText(str(int(current_filecount_num) - 1))
            current_filecount_num = self.file_count.text()
            self.file_count_3.setText(current_filecount_num)
            progress_count += 1
            self.move_progress.setValue((progress_count * 100) // labeled_count )
        try:
            self.dir_list.setCurrentCell(0, 0)
            self.show_image()
        except:
            pass


    def repair_key_event(self):
        # QMessageBox.warning(self, 'OK', '완료')
        self.repair_keyevent.setFocus()


if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
#%%
