import sys
from PyQt5.Qt import QVBoxLayout, QListWidget, QWidget,QPushButton,QHBoxLayout, QLabel, QMessageBox, QLineEdit,QCheckBox, QThread, QListWidgetItem
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd
import time
import pybit
from pybit.unified_trading import HTTP
import main
import os
import json
import time
import threading


class App(QWidget):
    def __init__(self):
        super(App,self).__init__()
        self.setWindowTitle("ByBit")


        self.cheak_test = False
        self.key = None
        self.bid= None
        self.secret= None


        self.windget()

    def get_price(self):
        time= self.get_time()
        session = HTTP(testnet=self.cheak_test)
        self.cheaking_price=session.get_kline(
            category="spot",
            symbol="BTCUSDT",
            interval=1,
            start=time-60000,
            end=time,
            limit=1,
        )

        self.coorse = float(self.cheaking_price['result']['list'][0][4])



        


    def windget(self):
        self.label_1=QLabel("Введите api-ключ")
        self.label_2 = QLabel("Введите секретный ключ")
        self.label_3 = QLabel("Введите вашу ставку($)")

        self.input_key = QLineEdit()
        self.input_key.textChanged[str].connect(self.onChanged_key)

        self.input_secret_key = QLineEdit()
        self.input_secret_key.textChanged[str].connect(self.onChanged_secret_key)

        self.input_bid = QLineEdit()
        self.input_bid.textChanged[str].connect(self.onChanged_bid)

        self.get_price()
        self.price = QPushButton(f"1BTC = {self.coorse}USDT")

        self.test = QCheckBox("test-net")
        self.test.stateChanged.connect(self.check_Answer)

        self.start = QPushButton("Включить")
        self.start.clicked.connect(self.cheak_ready)

        self.terminal = QListWidget()
        self.terminal.setStyleSheet("background-color: black; color: rgb(209,209,209);")

        #self.profit = QPushButton()
        #self.thread.about_status2.connect(self.profit.setText)

        self.get_password()

        layout1 = QVBoxLayout(self)

        layout3 = QHBoxLayout(self)
        layout3.addWidget(self.label_1)
        layout3.addWidget(self.test)

        layout1.addLayout(layout3)
        layout1.addWidget(self.input_key)
        layout1.addWidget(self.label_2)
        layout1.addWidget(self.input_secret_key)     
        layout1.addWidget(self.label_3)

        layout2 = QHBoxLayout(self)
        layout2.addWidget(self.input_bid)
        layout2.addWidget(self.price)

        layout1.addLayout(layout2)
        layout1.addWidget(self.start)
        layout1.addWidget(self.terminal)
        
        

    def onChanged_key(self, text):

        self.input_key.setText(text)
        self.input_key.adjustSize()

        self.key = text

    def onChanged_secret_key(self, text):

        self.input_secret_key.setText(text)
        self.input_secret_key.adjustSize()

        self.secret = text

    def onChanged_bid(self, text):

        self.input_bid.setText(text)
        self.input_bid.adjustSize()
        if text!= None and self.is_number(text) :
            self.price.setText(f"{round(float(text)/self.coorse, 4)}BTC = {text}")

        self.bid = text

    def check_Answer(self, state):

        if state == QtCore.Qt.Checked:
            self.cheak_test = True
        else:
            self.cheak_test = False
        self.get_price()
        if self.bid != None and self.is_number(self.bid) :
            self.price.setText(f"{round(float(self.bid)/self.coorse, 4)}BTC = {self.bid}")
        else:
            self.price.setText(f"1BTC = {self.coorse}USDT")


    def is_number(self, stroka: str):
        try:
            float(stroka)
            return True
        except ValueError:
            return False

    def cheak_ready(self):
        try:
            if self.key== None or self.secret == None or self.bid == None:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText(f"Введите данные")
                msgBox.setWindowTitle("ERROR")
                msgBox.setStandardButtons(QMessageBox.Ok)

                x=msgBox.exec_()
            else :
                self.save_password()
                #self.thread = main.Trade(self.key,self.secret, self.bid, self.cheak_test)
                #self.thread.about_status1.connect(self.terminal.setText)
                #self.thread.start()
                self.tread = main.Trade(self.key,self.secret, round(float(self.bid)/self.coorse, 4), self.cheak_test,w)

        except pybit.exceptions.InvalidRequestError as e:
            self.terminal.addItem(str(e))

        except ValueError as e:
            self.terminal.addItem(f"Проверьте правильность ввода данных\nОшибка:\n{e}")


    def get_password(self):
        try:
            dir = rf"{os.path.abspath(__file__)}"
            index = str(dir).rfind('\\')
            pooti = os.path.abspath(__file__)[:index]+"\\password.txt"
                          
        
            f = open(rf'{pooti}', 'r')
            txt= f.read()
            if txt != "":
            
                self.key, self.secret = txt.split("\n")

                self.input_key.setText(self.key)
                self.input_secret_key.setText(self.secret)
            f.close()
        except FileNotFoundError as e:
            dir = rf"{os.path.abspath(__file__)}"
            index = str(dir).rfind('\\')
            pooti = os.path.abspath(__file__)[:index]+"\\password.txt"
                          
        
            f = open(rf'{pooti}', 'w+')
            f.close()


    def save_password(self):
        dir = rf"{os.path.abspath(__file__)}"
        index = str(dir).rfind('\\')
        pooti = os.path.abspath(__file__)[:index]+"\\password.txt"
                          
        
        f = open(rf'{pooti}', 'r+', encoding='utf-8')
        f.write(f"{self.key}\n{self.secret}")
        f.close()

    def get_time(self):
        return round(time.time() * 1000)
    
    def closeEvent(self):
        sys.exit()
            

            
    




app = QtWidgets.QApplication(sys.argv)
w = App()
w.resize(500, 300)
w.show()
sys.exit(app.exec_())
        