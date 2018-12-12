import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm


import tkinter as Tkinter
import tkinter.font as tkFont


import threading


# =============================================================================
# interface
# =============================================================================


# =============================================================================
# Client
# =============================================================================

class Client():
    title = 'ICS Chat System' 
    
    def __init__(self, args):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        
    #interface    
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
        self.sendButton=Tkinter.Button(self.frame[3],text=' Send ',width=10,command=self.sendM())  
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)  
  
        #關閉按鈕  
        self.closeButton=Tkinter.Button(self.frame[3],text=' Quit ',width=10,command=self.close)  
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=15,pady=8)  
        self.frame[3].pack(expand=1,fill=Tkinter.BOTH)  
    
    def close(self):  
        sys.exit()

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()

    def shutdown_chat(self):
        return
    
    def sendM(self):
        message = self.inputText.get('1.0',Tkinter.END).encode() 
        try:
            self.send(message)
            self.chatText.insert(Tkinter.END,'  ' + message.decode() + '\n')   
            self.inputText.delete(0.0,message.__len__()-1.0) 
        except:
            self.chatText.insert(Tkinter.END,'  ' + message.decode() + '\n')   
            self.inputText.delete(0.0,message.__len__()-1.0) 

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def output(self):
        if len(self.system_msg) > 0:
            self.chatText.insert(Tkinter.END,'  ' + self.system_msg + '\n') 
            
            self.system_msg = ''

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = json.dumps({"action":"login", "name":self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)


    def read_input(self):
        while True:
            text = self.inputText.get('1.0',Tkinter.END)
            if text == '':
                continue
            else:
                
#            text = sys.stdin.readline()[:-1]
                self.chatText.insert(Tkinter.END,'  a' + text + '\n')
                self.console_input.append(text) # no need for lock, append is thread safe
                continue
                
    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()


#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)
