# Đã check dc thuật toán bắt serial trùng khi file debug thay đổi dung lượng
# -> xuat ra giao dien GUI
# Tim cach tao lai thread bằng QTthread



from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtWidgets
import sys
import datetime
from time import strftime,localtime
import pandas as pd
from Interface import Ui_MainWindow
from convert_txt_to_csv import *
from time import sleep
from threading import Thread
import threading

#global trigger_auto

class Page1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win1 = QMainWindow()
        self.page1 = Ui_MainWindow()
        self.page1.setupUi(self.win1)
        self.win1.setFixedHeight(269)
        self.win1.setFixedWidth(722)
        self.win1.show()

class BackEnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.trigger_auto = 0
        self.trigger_check = 0
    
    def relation_csv_to_list(self):
        copy_txt_file()
        convert_csv()
        #Get cot thu 8 in to list python
        ##Dat ten cho column
        # column_names = ["Date","Time","AMPM","ROWS","numROW","COLUMN","numColumn","Serial"]
        # df = pd.read_csv("debug.csv",names=column_names)
        # test = df.coul
        data = pd.read_csv("debug.csv")
        serial = data['7'].to_list()
        # print(serial)
        return serial
    

    def find_duplicates(self,list_serial):
        duplicates = []
        for number in list_serial:
            if list_serial.count(number) > 1:
                duplicates.append(number) 
        #duplicates = [number for number in list_serial if list_serial.count(number) > 1]
        unique_duplicates = list(set(duplicates))
        print(unique_duplicates)


        indices = []
        for (index,item) in enumerate(list_serial):
            for test in unique_duplicates:
                if item == test:
                    indices.append(index)
            
        print("Result: ",indices)
        odd_index_list = []
        for odd_index in indices:
            if indices.index(odd_index) %2 == 1:
                odd_index_list.append(odd_index)
        print("Odd index list: ",odd_index_list)

        return odd_index_list

    def display_ui(self,position_duplicate):
        data = pd.read_csv("debug.csv")
        display_ui_date = data.iat[5,0] #Hàng 5 cột 0
        display_ui_time = data.iat[5,1]
        display_ui_AMPM = data.iat[5,2]
        display_ui_row = data.iat[5,4]
        display_ui_column = data.iat[5,6]
        display_ui_serial = data.iat[5,7]
        
        #Display UI front-end
        w.page1.Time_duplicate.setText(display_ui_date + display_ui_time + display_ui_AMPM)
        # w.page1.row_duplicate.setText(display_ui_row)
        # w.page1.column_duplicate.setText(display_ui_column)
        # w.page1.serial_duplicate.setText(display_ui_serial)
        print("Thoi gian trung: ",display_ui_date + display_ui_time + display_ui_AMPM)
        print("Hang: ",display_ui_row)
        print("Cot: ",display_ui_column)
        print("Serial: ",display_ui_serial)

        w.page1.Confirm_ignore.setEnabled(True)

        #Delete index in odd_index_list
        # data = data.drop(labels=[5],axis=0)
        # data = data.to_csv("debug2.csv")

    def Manual_check(self):
        print("MANUAL CHECK")

def check_status_debugfile():
    try:
        # print(w.page1.Auto_check_box.checkState())
        pre_size = 0 #os.stat('debug.txt').st_size
        while True:
            if w.page1.Auto_check_box.checkState() == 2:
                # print(w.page1.Auto_check_box.checkState())
                file_stat = os.stat('debug.txt')
                size = file_stat.st_size
                print("pre_size: ",size)
                if size - pre_size != 0:
                    print("Trigger check 1")
                    run_algorithm.trigger_check = 1
                else:
                    print("Trigger check 0")
                    run_algorithm.trigger_check = 0     
                pre_size = size  
                sleep(2)

            else:
                print(w.page1.Auto_check_box.checkState())
                #Enalble button manual check
                w.page1.manual_check.setEnabled(True)
                w.page1.manual_check.clicked.connect(run_algorithm.Manual_check)
            sleep(1)
    except KeyboardInterrupt:
        exit(0)

def main_thread():
    while True:
        if run_algorithm.trigger_check == 1:
            print("Process 1 lan") 
            serial_number = run_algorithm.relation_csv_to_list()
            index_duplicate = run_algorithm.find_duplicates(serial_number)
            run_algorithm.display_ui(index_duplicate)
            run_algorithm.trigger_check = 0
            
        # else:
        #     print("WAITING PROCESSING")


if __name__ == '__main__':
    try:
        
        app = QApplication(sys.argv)
        w = Page1()
        
        t1 = threading.Thread(target=main_thread,args=())
        run_algorithm = BackEnd()
        # t3 = threading.Thread(target=check_auto_mode,args=())
        t2 = threading.Thread(target=check_status_debugfile,args=())
        
        t1.start()
        # t3.start()
        t2.start()
        
        sys.exit(app.exec())

        
    except KeyboardInterrupt:
        t1.join()
        t2.join()
        # t3.join()
        print("Error")