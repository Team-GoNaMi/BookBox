from tkinter import *
import tkinter.font
import tkinter
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import cv2
import copy
import RPi.GPIO as GPIO
from qr_Recognize import *
from locker import *
from barcode_Recognize import *
from connect_database import *

#Fontmain = tkinter.font.Font(family = 'Helvetica', size = 24, weight = 'bold')
#Fontbutton = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')

class GuiGui ():
    
    def __init__(self) :
        self.recognition = CodeRecognition()
        self.locker = Locker()
        self.bar_recog = BarRecognition()
        
    
    def closing_allGui(self, gui):
        gui.quit()
    
    def closing(self, gui):
        gui.iconify()

    def WELCOME_GUI(self):
        self.Gui_welcome = Tk()
        self.Gui_welcome.title("BBB_WELCOME")
        self.Gui_welcome.config(background= "#CEF279")
        self.Gui_welcome.geometry("800x430+0+0")
        self.Gui_welcome.resizable(0,0)
        
        Font1 = tkinter.font.Font(family = 'Helvetica', size = 24, weight = 'bold')
        
        Text1 = Label(self.Gui_welcome,text='북박북에 오신 걸 환영합니다~!', font= Font1, fg='black', bg = '#CEF279', padx = 200, pady = 150)
        Text1.grid(row=0,column=0)

        StartButton= Button(self.Gui_welcome, text='이용하기!', command = self.QR_GUI, fg='black', height = 1, width = 10, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        StartButton.grid(row = 1, column =0)

        #self.Gui_welcome.mainloop()
        
    
    # QR Recognition page
    def QR_GUI(self):
#        self.Gui_qr = Tk()
        self.Gui_qr = Toplevel(self.Gui_welcome)
        self.Gui_qr.title("BBB_QR")
        self.Gui_qr.config(background= "#CEF279")
        self.Gui_qr.geometry("800x430+0+0")
        self.Gui_qr.resizable(0,0)
        
        Font1 = tkinter.font.Font(family = 'Helvetica', size = 24, weight = 'bold')
 
        
        Text1 = Label(self.Gui_qr,text='큐알코드를 인식해주세요 ;)', font= Font1, fg='black', bg = '#CEF279', padx = 200, pady = 150)
        Text1.grid(row=0,column=0)

        StartButton= Button(self.Gui_qr, text='인식하기!', command = self.close_and_qr, fg='black', height = 1, width = 10, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        StartButton.grid(row = 1, column =0)
    

    def close_and_qr(self) :
        self.Gui_qr.iconify()
        self.recognition.gogoSing()
        #self.Gui_no.deiconify()
        
        success = self.recognition.get_success()
        print(success, "!!hello")
        self.isSeller = self.recognition.isSeller()

        #seller
        if(success and self.isSeller):
            print("!!seller")
            self.BARCODE_GUI()
    
        #buyer
        elif(success and self.isSeller == False):
            print("!!buyer")
            self.BOX_GUI()
    
        #no reservation
        elif(success == False):
            print("!!not found")
            self.NOTFOUND_GUI()
            #self.Gui_no.iconify()
        
    
    # Barcode Recognition page -> only if user is a seller
    def BARCODE_GUI(self):
        self.Gui_bar = Toplevel(self.Gui_welcome)
        self.Gui_bar.title("BBB_BAR")
        self.Gui_bar.config(background= "#CEF279")
        self.Gui_bar.geometry("800x430+0+0")
        self.Gui_bar.resizable(0,0)
        Font1 = tkinter.font.Font(family = 'Helvetica', size = 24, weight = 'bold')

        Text1 = Label(self.Gui_bar,text='책의 바코드를 인식해주세요 ;)',font=Font1, fg='black', bg = '#CEF279', padx = 200, pady = 150)
        Text1.grid(row=0,column=0)

        StartButton= Button(self.Gui_bar, text='인식하기!', command = self.close_and_bar, fg='black', height = 1, width = 10, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        StartButton.grid(row = 1, column =0)
        #CloseButton= Button(self.Gui_bar, text='창 닫기', command = self.close_and_bar, fg='black', height = 1, width = 10, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        #CloseButton.grid(row = 2, column =0) 

    def close_and_bar(self) :
        self.Gui_bar.iconify()
        self.bar_recog.gogoRing()
        
        o_isbn = self.recognition.get_barcode()
        isbn = self.bar_recog.get_barcode()
        
        print(o_isbn, "ohohoh!!")
        print(isbn, "!!ohohoh")

        #seller
        if(isbn == o_isbn):
            print("!!seller")
            self.BOX_GUI()
            
    
        #no reservation
        else:
            print("!!not this book")
            self.NOTTHISBOOK_GUI()
        
    def NOTTHISBOOK_GUI(self):
        self.Gui_notBook = Toplevel(self.Gui_welcome)
        self.Gui_notBook.title("BBB_NOTBOOK")
        self.Gui_notBook.config(background= "#CEF279")
        self.Gui_notBook.geometry("800x430+0+0")
        self.Gui_notBook.resizable(0,0)
        Font1 = tkinter.font.Font(family = 'Helvetica', size = 24, weight = 'bold')

        Text1 = Label(self.Gui_notBook,text='이 책이 확실한가요..? :(\n다시 한 번 인식해주세요ㅠㅠ', font = Font1, fg='black', bg = '#CEF279', padx = 200, pady = 130)
        Text1.grid(row=0,column=0)

        StartButton= Button(self.Gui_notBook, text='다시 인식하기!', command = self.close_and_notThis, fg='black', height = 1, width = 15, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        StartButton.grid(row = 1, column =0)
        CloseButton= Button(self.Gui_notBook, text='처음 페이지로 돌아가기', command = self.close_and_notBook, fg='black', height = 1, width = 15, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        CloseButton.grid(row = 2, column =0) 

    def close_and_notThis(self):
        self.Gui_notBook.iconify()
        self.Gui_bar.deiconify()
    
    def close_and_notBook(self) :
        self.Gui_notBook.iconify()
        #self.Gui_qr.deiconify()
        
    # Box page
    def BOX_GUI(self):
        self.Gui_box = Toplevel(self.Gui_welcome)
        self.Gui_box.title("BBB_BOX")
        self.Gui_box.config(background= "#CEF279")
        self.Gui_box.geometry("800x430+0+0")
        self.Gui_box.resizable(0,0)
        Font1 = tkinter.font.Font(family = 'Helvetica', size = 24, weight = 'bold')
        box_id = self.recognition.get_box_id()
        Text1 = Label(self.Gui_box,text= box_id+'번 북박스입니다!\n 이용 후 잠금버튼을 눌러주세요;)', font = Font1, fg='black', bg = '#CEF279', padx = 200, pady = 100)
        Text1.grid(row=0,column=0)
        
        UnlockButton= Button(self.Gui_box, text='열기', command = self.close_and_unlock, fg='black', height = 1, width = 10, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        UnlockButton.grid(row = 1, column =0)
        LockButton= Button(self.Gui_box, text='잠그기', command = self.close_and_lock, fg='black', height = 1, width = 10, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        LockButton.grid(row = 2, column =0)
    
    def close_and_unlock(self):
        self.locker.unlock()
    
    def close_and_lock(self) :
        # Update trade state
        db_connection = ConnectDB()
        register_id = self.recognition.get_register_id()
        print(register_id)
        db_connection.update_trade_state(register_id, self.isSeller)
        
        self.locker.lock()
        self.Gui_box.iconify()
        
        if(self.isSeller):
            print("!!seller")
            self.THANK_GUI()
    
        #buyer
        else:
            print("!!buyer")
            self.INFORM_GUI()
            
# Infrom page for buyer
    def INFORM_GUI(self):
        self.Gui_info = Toplevel(self.Gui_welcome)
        self.Gui_info.title("BBB_INFO")
        self.Gui_info.config(background= "#CEF279")
        self.Gui_info.geometry("800x430+0+0")
        self.Gui_info.resizable(0,0)
        Font1 = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')

        Text1 = Label(self.Gui_info,text='이용해주셔서 감사합니다:)', font = Font1, fg='black', bg = '#CEF279', padx = 200, pady = 50)
        Text1.grid(row=0,column=0)

        Text2 = Label(self.Gui_info,text='앱을 통하여 구매확정을 하거나 \n 책에 심각한 문제가 있을 시 신고를 해주세요!', font = Font1, fg='black', bg = '#CEF279', padx = 170, pady = 50)
        Text2.grid(row=1,column=0)
        
        #CloseButton= Button(self.Gui_info, text='처음 페이지로 돌아가기', command = self.close_and_info, fg='black', height = 1, width = 15, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        #CloseButton.grid(row = 2, column =0)
        
    
    def close_and_info(self) :
        self.Gui_info.iconify()
        #self.Gui_qr.deiconify()
        
    # Notfound page
    def NOTFOUND_GUI(self):
        
        self.Gui_no = Toplevel(self.Gui_welcome)
        self.Gui_no.title("BBB_NOTFOUND")
        self.Gui_no.config(background= "#CEF279")
        self.Gui_no.geometry("800x430+0+0")
        self.Gui_no.resizable(0,0)
        
        Font1 = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')

        Text1 = Label(self.Gui_no,text='예약정보가 없네요!', font = Font1, fg='black', bg = '#CEF279', padx = 240, pady = 50)
        Text1.grid(row=0,column=0)

        Text2 = Label(self.Gui_no,text='다시 한 번 확인해주세요:D', font = Font1, fg='black', bg = '#CEF279', padx = 200, pady = 50)
        Text2.grid(row=1,column=0)
        
        CloseButton= Button(self.Gui_no, text='처음 페이지로 돌아가기', command = self.close_and_no, fg='black', height = 1, width = 16, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        CloseButton.grid(row = 2, column =0)
        
        
    def close_and_no(self) :
        self.Gui_no.iconify()
        #self.Gui_qr.deiconify()
    
    #Thank page for seller
    def THANK_GUI(self):
        self.Gui_thank = Toplevel(self.Gui_welcome)
        self.Gui_thank.title("BBB_THANK")
        self.Gui_thank.config(background= "#CEF279")
        self.Gui_thank.geometry("800x430+0+0")
        self.Gui_thank.resizable(0,0)
        Font1 = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')
    
        Text1 = Label(self.Gui_thank,text='이용해주셔서 감사합니다!', font = Font1, fg='black', bg = '#CEF279', padx = 250, pady = 150)
        Text1.grid(row=0,column=0)
        
        #CloseButton= Button(self.Gui_thank, text='처음 페이지로 돌아가기', command = self.close_and_thank, fg='black', height = 1, width = 15, highlightbackground = '#FFFFFF', activebackground = '#FEC19E')
        #CloseButton.grid(row = 2, column =0)
    

        
    def close_and_thank(self) :
        self.Gui_thank.iconify()
        #self.Gui_qr.deiconify()
        
#    def get_success(self) :
#        print(self.recognition.get_success(),"ddd")
#        return self.recognition.get_success()
#    
#    def get_box_id(self) :
#        return self.recognition.get_box_id()
#    
#    def get_barcode(self) :
#        return self.recognition.get_barcode()
#    
#    def isSeller(self) :
#        return self.recognition.isSeller()
        

    
