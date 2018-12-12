#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 20:31:38 2018

@author: selinaxie
"""

import tkinter as Tkinter
import tkinter.font as tkFont

class interface():
    title = 'ICS Chat System'  
      
    def __init__(self):  
        self.root = Tkinter.Tk()  
        self.root.title(self.title)  
          
        #窗口面板,用4個面板布局  
        self.frame = [Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame()]  
  
        #顯示消息Text右邊的滾動條  
        self.chatTextScrollBar = Tkinter.Scrollbar(self.frame[0])  
        self.chatTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)  
          
        #顯示消息Text，並綁定上面的滾動條  
        ft = tkFont.Font(family="Fixdsys",size=11)  
        self.chatText = Tkinter.Listbox(self.frame[0],width=70,height=18,font=ft)  
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set  
        self.chatText.pack(expand=1,fill=Tkinter.BOTH)  
        self.chatTextScrollBar['command'] = self.chatText.yview()  
        self.frame[0].pack(expand=1,fill=Tkinter.BOTH)  
          
        #標簽，分開消息顯示Text和消息輸入Text  
        label = Tkinter.Label(self.frame[1],height=2)  
        label.pack(fill=Tkinter.BOTH)  
        self.frame[1].pack(expand=1,fill=Tkinter.BOTH)  
          
        #輸入消息Text的滾動條  
        self.inputTextScrollBar = Tkinter.Scrollbar(self.frame[2])  
        self.inputTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)  
          
        #輸入消息Text，並與滾動條綁定  
        ft = tkFont.Font(family='Fixdsys',size=11)  
        self.inputText = Tkinter.Text(self.frame[2],width=70,height=8,font=ft)  
        self.inputText['yscrollcommand'] = self.inputTextScrollBar.set  
        self.inputText.pack(expand=1,fill=Tkinter.BOTH)  
        self.inputTextScrollBar['command'] = self.chatText.yview()  
        self.frame[2].pack(expand=1,fill=Tkinter.BOTH)  
          
        #發送消息按鈕  
        self.sendButton=Tkinter.Button(self.frame[3],text=' Send ',width=10,command=self.sendMessage)  
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)  
  
        #關閉按鈕  
        self.closeButton=Tkinter.Button(self.frame[3],text=' Quit ',width=10,command=self.close)  
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=15,pady=8)  
        self.frame[3].pack(expand=1,fill=Tkinter.BOTH)  

    #發送消息  
    def sendMessage(self):  
        #得到用戶在Text中輸入的消息  
        message = self.inputText.get('1.0',Tkinter.END) 
        #格式化當前的時間  
#        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
#        self.chatText.insert(Tkinter.END, '客戶端器 ' + theTime +' 說：\n')  
        self.chatText.insert(Tkinter.END,'  ' + message + '\n')  
#        if self.flag == True:  
#            #將消息發送到服務器端  
#            self.clientSock.send(message);  
#        else:  
#            #Socket連接沒有建立，提示用戶  
#            self.chatText.insert(Tkinter.END,'您還未與服務器端建立連接，服務器端無法收到您的消息\n')  
        #清空用戶在Text中輸入的消息  
        self.inputText.delete(0.0,message.__len__()-1.0)  
        return message
      
    #關閉消息窗口並退出  
    def close(self):  
        sys.exit()  
        
    def run(self):
        self.root.mainloop()
