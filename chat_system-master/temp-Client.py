#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 17:12:09 2018

@author: selinaxie
"""

# _*_ coding:utf-8 _*_  
# Filename:ClientUI.py  
# Python在線聊天客戶端  
  
import tkinter as Tkinter
import tkinter.font as tkFont
import socket  
import _thread as thread 
import time  
import sys  
  
class ClientUI():  
      
    title = 'Python在線聊天-客戶端V1.0'  
    local = '127.0.0.1'  
    port = 8808  
    global clientSock;  
    flag = False  
      
    #初始化類的相關屬性，類似於Java的構造方法  
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
        self.closeButton=Tkinter.Button(self.frame[3],text=' Terminate ',width=10,command=self.close)  
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=15,pady=8)  
        self.frame[3].pack(expand=1,fill=Tkinter.BOTH)  
          
    #接收消息  
    def receiveMessage(self):  
        try:  
            #建立Socket連接  
            self.clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
            self.clientSock.connect((self.local, self.port))  
            self.flag = True  
        except:  
            self.flag = False  
            self.chatText.insert(Tkinter.END,'您還未與服務器端建立連接，請檢查服務器端是否已經啟動')  
            
            return  
              
        self.buffer = 1024  
        self.clientSock.send('Y'.encode())  
        while True:  
            try:  
                if self.flag == True:  
                    #連接建立，接收服務器端消息  
                    self.serverMsg = self.clientSock.recv(self.buffer).decode()  
                    if self.serverMsg == 'Y':  
                        self.chatText.insert(Tkinter.END,'客戶端已經與服務器端建立連接......')  
                    elif self.serverMsg == 'N':  
                        self.chatText.insert(Tkinter.END,'客戶端與服務器端建立連接失敗......')  
                    elif not self.serverMsg:  
                        continue  
                    else:  
                        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
                        self.chatText.insert(Tkinter.END, '服務器端 ' + theTime +' 說：\n')  
                        self.chatText.insert(Tkinter.END, '  ' + self.serverMsg)  
                else:  
                    break  
            except:
                raise EOFError() 
                self.clientSock.close()  
                break  
                    
    #發送消息  
    def sendMessage(self):  
        #得到用戶在Text中輸入的消息  
        message = self.inputText.get('1.0',Tkinter.END).encode()  
        #格式化當前的時間  
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
        self.chatText.insert(Tkinter.END, '客戶端器 ' + theTime +' 說：\n')  
        self.chatText.insert(Tkinter.END,'  ' + message.decode() + '\n')  
        if self.flag == True:  
            #將消息發送到服務器端  
            self.clientSock.send(message);  
        else:  
            #Socket連接沒有建立，提示用戶  
            self.chatText.insert(Tkinter.END,'您還未與服務器端建立連接，服務器端無法收到您的消息\n')  
        #清空用戶在Text中輸入的消息  
        self.inputText.delete(0.0,message.__len__()-1.0)  
      
    #關閉消息窗口並退出  
    def close(self):  
        sys.exit()  
      
    #啟動線程接收服務器端的消息  
    def startNewThread(self):  
        #啟動一個新線程來接收服務器端的消息  
        #thread.start_new_thread(function,args[,kwargs])函數原型，  
        #其中function參數是將要調用的線程函數，args是傳遞給線程函數的參數，它必須是個元組類型，而kwargs是可選的參數  
        #receiveMessage函數不需要參數，就傳一個空元組  
        thread.start_new_thread(self.receiveMessage,())  
  
def main():  
    client = ClientUI()  
    client.startNewThread()  
    client.root.mainloop()  
      
if __name__=='__main__':  
    main()  