# Author: On Tu Quoc Dat - Control System Engineer
# Company : Sonion Viet Nam Co.,Ltd
# Version : 1.0
# Update: 01/04/2023
# Built = Python 3.10.7 

#Special command python -m PyQt5.uic.pyuic -x inteface.ui -o interface.py



from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import QThread,QObject,pyqtSignal,QRunnable,pyqtSlot
from PyQt5 import QtWidgets,QtCore
import sys
import datetime
from time import strftime,localtime
import pandas as pd
from Interface import Ui_MainWindow
from convert_txt_to_csv import *
from time import sleep
from warning import *
import shutil
#global trigger_auto

class Page1(QMainWindow):
    setText_example = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.win1 = QMainWindow()
        self.page1 = Ui_MainWindow()
        self.page1.setupUi(self.win1)
        self.win1.setFixedHeight(269)
        self.win1.setFixedWidth(722)
        self.setText_example.connect(self.test)
        self.wait_val = 1
        self.win1.show()
        self.display_datetime = None
        self.display_row = None
        self.display_column = None
        self.display_serial = None

        self.page1.Confirm_ignore.clicked.connect(self.delete_duplicate)

    def delete_duplicate(self):
        ignore_complete()
        self.setText_example.emit()
        self.display_datetime = None
        self.display_row = None
        self.display_column = None
        self.display_serial = None 
        self.page1.Time_duplicate.setText("")
        self.page1.row_duplicate.setText("")
        self.page1.column_duplicate.setText("")
        self.page1.serial_duplicate.setText("")
        # data = pd.read_csv("debug_copy.csv")
        # data_save = data.drop(labels=[self.index_dup],axis=0)
        # data_save.to_csv("debug.csv",index=False)

        self.page1.Confirm_ignore.setEnabled(False)
        self.wait_val = 0

    @pyqtSlot()
    def test(self):
        pop_up_warning()
        self.page1.Time_duplicate.setText(self.display_datetime)
        self.page1.row_duplicate.setText(str(self.display_row))
        self.page1.column_duplicate.setText(str(self.display_column))
        self.page1.serial_duplicate.setText(self.display_serial)
        self.page1.Confirm_ignore.setEnabled(True)

        # return True
        
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
        # self.copy_data = data.copy()
        # self.copy_data.to_csv("debug_copy.csv",index=False)
        serial = data['7'].to_list()
        # print(serial)
        return serial#,self.copy_data
    

    def find_duplicates(self,list_serial):
        duplicates = []
        for number in list_serial:
            if list_serial.count(number) > 1:
                duplicates.append(number) 
        #duplicates = [number for number in list_serial if list_serial.count(number) > 1]
        unique_duplicates = list(set(duplicates))
        # if len(unique_duplicates) > 0:
        #     pop_up_warning()
        print(unique_duplicates)

        #
        indices = []
        for (index,item) in enumerate(list_serial):
            for test in unique_duplicates:
                if item == test:
                    indices.append(index)
        #

        save_dup = {}
        max_value = []
        for i in range (0,len(unique_duplicates)):
            save_dup['Dup' +str(i)] = []
        # print(save_dup['Dup1'])
            for j in range(0,len(list_serial)):
                # for k in range(0,len(unique_duplicates)):
                if list_serial[j] == unique_duplicates[i]:
                    # print("List serial: ",[j])
                    # print("List unique duplicate: ",[i])
                    save_dup['Dup'+str(i)].append(j)
            max_value.append(max(save_dup['Dup' +str(i)]))
        # print("MAX VALUE: ",max_value)

        # print("Dup1: ",max(save_dup['Dup'+str(0)]))
        # print("Dup2: ",max(save_dup['Dup'+str(1)]))

        return max_value




    def display_ui(self,position_duplicate):
        self.data = pd.read_csv("debug.csv")

        display_ui_date = self.data.iat[position_duplicate,0] #Hàng 5 cột 0
        display_ui_time = self.data.iat[position_duplicate,1]
        display_ui_AMPM = self.data.iat[position_duplicate,2]
        display_ui_row = self.data.iat[position_duplicate,4]
        display_ui_column = self.data.iat[position_duplicate,6]
        display_ui_serial = self.data.iat[position_duplicate,7]
        
        w.display_datetime = str(display_ui_date + display_ui_time + display_ui_AMPM)
        w.display_row = str(display_ui_row)
        w.display_column = str(display_ui_column)
        w.display_serial = str(display_ui_serial)

        # print("Thoi gian trung: ",display_ui_date + display_ui_time + display_ui_AMPM)
        # print("Hang: ",display_ui_row)
        # print("Cot: ",display_ui_column)
        # print("Serial: ",display_ui_serial)

        
        #Delete index in odd_index_list
        # self.data = self.data.drop(labels=[position_duplicate],axis=0)
        # self.data = self.data.to_csv("debug.csv")
        # return display_datetime,display_row,display_column,display_serial
    def Manual_check(self):
        print("MANUAL CHECK")

class Worker2(QObject):
    finished2 = pyqtSignal()
    progress2 = pyqtSignal(int)

    def check_status_debugfile(self):
        src_debug = 'debug.txt'
        #dst_debug = 'debug_process.txt'
        try:
            # print(w.page1.Auto_check_box.checkState())
            pre_size = 0 #os.stat('debug.txt').st_size
            while True:
                w.page1.manual_check.setEnabled(False)
                if w.page1.Auto_check_box.checkState() == 2:
                    #shutil.copyfile(src_debug,dst_debug)
                    # print(w.page1.Auto_check_box.checkState())
                    file_stat = os.stat(src_debug)
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

class Worker1(QObject):
    finished1 = pyqtSignal()
    progress1 = pyqtSignal(int)
    gui_display = pyqtSignal()
    def __init__(self):
        super().__init__()
    def main_thread(self):
        while True:
            if run_algorithm.trigger_check == 1:
                #Pop 
                print("Process 1 lan") 
                serial_number = run_algorithm.relation_csv_to_list()
                index_duplicate = run_algorithm.find_duplicates(serial_number)
                data = pd.read_csv("debug.csv")
                for w.index_dup in index_duplicate:
                    w.wait_val = 0
                    run_algorithm.display_ui(w.index_dup)
                    #Goi data tu main program display
                    w.setText_example.emit()
                    #Delete product in csv file
                    # run_algorithm.data = run_algorithm.data.drop(labels=[index_dup],axis=0)
                    # run_algorithm.data = run_algorithm.data.to_csv("debug.csv")                 
                    w.wait_val = 1
                    while w.wait_val == 1:
                        # print("Wait to press ignore")
                        pass
                #Đợi xác nhận hết rồi Xoa du lieu luon 1 lan
                for delete_index in index_duplicate:
                    data = data.drop(labels=[delete_index],axis=0)
                data.to_csv("debug.csv",index=False)

                #Xóa trên txt, hoàntất process
                print("INDEX DUPLICATE: ",index_duplicate)
                a_file = open("debug.txt","r")
                lines = a_file.readlines()
                a_file.close()
                #delete rows
                for i in range(0,len(index_duplicate)):
                    del lines[index_duplicate[i]]
                #write to new file
                new_file = open("debug.txt","w+")
                for line in lines:
                    new_file.write(line)
                new_file.close()
                
                run_algorithm.trigger_check = 0




if __name__ == '__main__':
    try:
        
        app = QApplication(sys.argv)
        # w = Page1()
        # run_algorithm = BackEnd()

        thread1 = QThread()
        worker_1 = Worker1()
        worker_1.moveToThread(thread1)
        


        thread2 = QThread()
        worker_2 = Worker2()
        worker_2.moveToThread(thread2)

        w = Page1()
        run_algorithm = BackEnd()

        thread1.started.connect(worker_1.main_thread)
        worker_1.finished1.connect(thread1.quit)
        worker_1.finished1.connect(thread1.deleteLater)
        thread1.finished.connect(thread1.deleteLater)
        

        thread2.started.connect(worker_2.check_status_debugfile)
        worker_2.finished2.connect(thread2.quit)
        worker_2.finished2.connect(thread2.deleteLater)
        thread2.finished.connect(thread2.deleteLater)

        thread1.start()
        thread2.start()
        # t1 = threading.Thread(target=main_thread,args=())
        # t2 = threading.Thread(target=check_status_debugfile,args=())
        
        # t1.start()
        # t3.start()
        # t2.start()
        
        
        sys.exit(app.exec())

        
    except KeyboardInterrupt:
        # t1.join()
        # t2.join()
        # t3.join()
        print("Error")