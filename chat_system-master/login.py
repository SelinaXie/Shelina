from tkinter import *
from tkinter import ttk

class Login():
    def __init__(self,master):
        #name
    
        self.name_label=ttk.Label(master,text='Name:')
        self.name_label.grid(row=0,column=0)  #左上name
        self.name_entry=ttk.Entry(master,width=18) 
        self.name_entry.grid(row=0,column=1,columnspan=5) #姓名输入框
        self.user_name=''

        
    
        #submit_button
        self.submit_button=ttk.Button(master,text='Login',command=self.make_profile)
        self.submit_button.grid(row=100,columnspan=10)

    
    def make_profile(self):
        self.user_name=self.name_entry.get()
        

    

def main():
    root=Tk()
    root.title('Enter your name to log in')
    login_interface = Login(root)
    while True:
        root.update()
        
if __name__=='__main__':
    main()
