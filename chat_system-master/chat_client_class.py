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
        self.root.geometry("600x600")
        self.root.resizable(width = False, height = False)
          
        #four windows
        self.frame = [Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame()]  
  
        #ScrollBar  
        self.chatTextScrollBar = Tkinter.Scrollbar(self.frame[0])  
        self.chatTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)  
          
        #Display Text along with the scroll bar
        ft = tkFont.Font(family="Arial",size=16)  
        self.chatText = Tkinter.Listbox(self.frame[0],width=50,height=18,font=ft)  
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set  
        self.chatText.pack(expand=1,fill=Tkinter.BOTH)  
        self.chatTextScrollBar['command'] = self.chatText.yview()  
        self.frame[0].pack(expand=1,fill=Tkinter.BOTH)  
          
        #labels
        label = Tkinter.Label(self.frame[1],height=2)  
        label.pack(fill=Tkinter.BOTH)  
        self.frame[1].pack(expand=1,fill=Tkinter.BOTH)  
          
        #inputBox ScrollBar
        self.inputTextScrollBar = Tkinter.Scrollbar(self.frame[2])  
        self.inputTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)  
          
        #input Text
        ft = tkFont.Font(family='Arial',size=16)  
        self.inputText = Tkinter.Text(self.frame[2],width=50,height=8,font=ft)  
        self.inputText['yscrollcommand'] = self.inputTextScrollBar.set  
        self.inputText.pack(expand=1,fill=Tkinter.BOTH)  
        self.inputTextScrollBar['command'] = self.chatText.yview()  
        self.frame[2].pack(expand=1,fill=Tkinter.BOTH)  
          
        #Send Button
        self.sendButton=Tkinter.Button(self.frame[3],text=' Send ',width=10,command=self.sendM)  
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)  
  
        #Quit Button 
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
        
        self.system_msg += 'Welcome to ICS chat! \n'
        self.output()
        self.system_msg += 'Please enter your name: '
        print('as1')
        self.output()
        print('as2')
        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        print('as3')
        self.output()

        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
            
  

    def shutdown_chat(self):
        return
    
    def sendM(self):
        message = self.newM()
        if self.read_input(message.decode()):
        
            try:
                self.send(message)
                self.chatText.insert(Tkinter.END,'  ' + message.decode() + '\n')   
                self.inputText.delete(0.0,message.__len__()-1.0) 
            except:
                self.chatText.insert(Tkinter.END,'  ' + message.decode() + '\n')   
                self.inputText.delete(0.0,message.__len__()-1.0) 
#        return message.decode()

    def send(self, msg):
        mysend(self.socket, msg)
        
    def newM(self):
        message = self.inputText.get('1.0',Tkinter.END).encode() 
        return message

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
        self.root.update() 

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        
        if len(my_msg) > 0:
            print(my_msg)
            self.name = my_msg
            print('name', self.name)
            msg = json.dumps({"action":"login", "name":self.name})
            print('here')
            self.send(msg)
            print('there')
            response = json.loads(self.recv())
            print('r',response)
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


    def read_input(self, text):
#        text = self.sendM()
        
        if len(text.strip())==0:
            
            return False
        else:
#                self.chatText.insert(Tkinter.END,'  hahah' + text + '2')
            
##            text = sys.stdin.readline()[:-1]
#                self.chatText.insert(Tkinter.END,'  a' + str(len(text)) + str(text == ' ') + '\n')
            self.console_input.append(text) # no need for lock, append is thread safe
            print('s',self.console_input)
            return True
            
            
                
    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        reading_thread = threading.Thread(target=self.init_chat)
        reading_thread.daemon = True
        reading_thread.start()
        
        
        print('as')
#        self.system_msg += 'Welcome to ICS chat\n'
#        self.system_msg += 'Please enter your name: '
#        print('as1')
#        self.output()
#        print('as2')
#        while self.login() != True:
#            self.output()
#        self.system_msg += 'Welcome, ' + self.get_name() + '!'
#        print('as3')
#        self.output()
#        self.root.mainloop()
#
#        while self.sm.get_state() != S_OFFLINE:
#            self.proc()
#            self.output()
#            time.sleep(CHAT_WAIT)

        self.root.mainloop()


#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)
        

#import argparse
#parser = argparse.ArgumentParser(description='chat client argument')
#parser.add_argument('-d', type=str, default=None, help='server IP addr')
#args = parser.parse_args()
#client = Client(args)
#root = client.root
#client.run_chat()
#
#root.mainloop()


