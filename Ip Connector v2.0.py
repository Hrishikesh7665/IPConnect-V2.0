from cryptography.fernet import Fernet
from tkinter import PhotoImage
from tkinter import messagebox
import win32con, win32api
#from tkinter import font
from tkinter import *
import sys,os
import time
import requests
#import getpass
import re
import validators
import webbrowser
import emoji
from bs4 import BeautifulSoup
key = Fernet(b'6nKlcr2i2gzFP7hURvHY_05158yINqTdRhDjW2nDm5E=')

#For Creat Button ToolTip
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

#------------------------------------------


#Get absolute path to resource, works for dev and for PyInstaller
def resource_path():
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # Look for the 'sprites' folder on the path I just gave you:
    spriteFolderPath = os.path.join(CurrentPath, 'Assets')
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath

_path = resource_path()
#print(_path)

# dictionary of colors:
color = {"nero": "#252726", "orange": "#FF8700", "darkorange": "#FE6101"}

# setting root window:
root = Tk()
root.title("IP Connect v2.0 (By Hrishikesh Patra)")
root.config(bg="gray17")
#root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=_path+"\ic_launcher.png"))
#root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=_path+"\Icon.png"))
root.wm_iconbitmap(_path+"/Icon.ico")
#root.geometry("400x600")


#openwindowcenter of screen every time
def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)  #change hs/2 to hs/4 to left window up
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
center_window(400, 600)

#MakeWindow Unrealizable

root.resizable(False, False)







show_username =StringVar()
show_username.set("User Not Logged In")
userId_Var =StringVar()
userId_Var.set("Hint: my_username")
userPass_Var =StringVar()
userPass_Var.set("Eneter Password Here")
userUrl_Var =StringVar()
userUrl_Var.set("Hint: 10.254.254.24/0/up/")
scrollText = StringVar()

show_user_address = StringVar()
show_user_client_ID = StringVar()
show_user_package = StringVar()
show_user_expiry_date = StringVar()
show_user_email = StringVar()
first_Time_check = ""
main_url =""
btn_st =""
v = "True"
failled_count = 0
# setting switch state:
btnState = False

# loading Navbar icon image:
navIcon = PhotoImage(file=_path+"\menu.png")
closeIcon = PhotoImage(file=_path+"\close.png")
logoIcon = PhotoImage(file=_path+"\logo.png")
eye_open = PhotoImage(file=_path+"\eye_open.png")
eye_close = PhotoImage(file=_path+"\eye_close.png")
home_icon = PhotoImage(file=_path+"\home_icon.png")
profile_icon = PhotoImage(file=_path+"\profile_icon.png")
about_icon = PhotoImage(file=_path+"\About_icon.png")
others_icon = PhotoImage(file=_path+"\others_icon.png")
exit_icon = PhotoImage(file=_path+"\exit_icon.png")
save_B = PhotoImage(file=_path+"\save_icon.png")
reset_B = PhotoImage(file=_path+"\Reset_icon.png")
pay_B = PhotoImage(file=_path+"\pay.png")
f_reset_B = PhotoImage(file=_path+"\del_icon.png")
#dev_icon = PhotoImage(file=_path+"\dev2.png")
Hackerrank_Icon = PhotoImage(file=_path+"\h.png")
github_Icon = PhotoImage(file=_path+"\github.png")
fb_Icon = PhotoImage(file=_path+"\Fb.png")

#Get Appdata path
appdata_path = os.getenv('APPDATA')

#root.iconphoto(False, main_logo)


#Check ForSaved Logininfo file if available readdata and decrypt the file,
#if file found but is tamperedelet the file
def check_login_file_avalability ():
    global first_Time_check
    en_file =appdata_path+"\encrypted.dat"
    try:
        temp = open(en_file,'r').read().split('\n')
        name_str = (temp[0])
        name = bytes(name_str, 'utf-8')

        password_str =temp[1]
        password = bytes(password_str, 'utf-8')

        url_str=temp[2]
        url = bytes(url_str, 'utf-8')

        Decrypted_name = key.decrypt(name)
        userId_Var.set(Decrypted_name.decode("utf-8"))
        #print(Decrypted_name)

        Decrypted_pass = key.decrypt(password)
        userPass_Var.set(Decrypted_pass.decode("utf-8"))
        #print(Decrypted_pass)
        upass_input.config(show="*")
        Decrypted_url = key.decrypt(url)
        userUrl_Var.set(Decrypted_url.decode("utf-8"))
        first_Time_check = False
        #print(Decrypted_url)

        #temp.close()
 #check file blank
    except:
        if os.path.exists((appdata_path +"\encrypted.dat")):
            os.remove(en_file)
        #en_file =appdata_path+"\encrypted.dat"
        #file1 = open(en_file,"wb")
        #win32api.SetFileAttributes(en_file,win32con.FILE_ATTRIBUTE_HIDDEN)
        #file1.close()
        #print("File")
        first_Time_check = True


#save login info to file after successfully user want to save and encrypt file
def save_login_info ():
    global first_Time_check
    #print("Hi")
    if first_Time_check == True:
        ans = messagebox.askyesno("Saved Log In Info", "Do You Want To Save Login Info\nFor Future Login?")
        if ans == True:
            remove_http = main_url[7:]
            encrypted_A = key.encrypt(bytes(userId_Var.get(), 'utf-8'))
            encrypted_B = key.encrypt(bytes(userPass_Var.get(), 'utf-8'))
            encrypted_C = key.encrypt(bytes(remove_http, 'utf-8'))
            en_file =appdata_path+"\encrypted.dat"
            if os.path.exists((appdata_path +"\encrypted.dat")):
                os.remove(en_file)
            file1 = open(en_file,"wb")
            L = [encrypted_A,encrypted_B,encrypted_C]
            file1.write(encrypted_A)
            file1.write(b"\n")
            file1.write(encrypted_B)
            file1.write(b"\n")
            file1.write(encrypted_C)
            win32api.SetFileAttributes(en_file,win32con.FILE_ATTRIBUTE_HIDDEN)
            file1.close()
            first_Time_check = False
            #print("Encryption successfull")
        if ans == False:
            #pass
            first_Time_check = False
    switch_wellcome_label(1)


#save login info to file after button click and encrypt file
def save_login_info_button_fun ():
    remove_http = main_url[7:]
    encrypted_A = key.encrypt(bytes(userId_Var.get(), 'utf-8'))
    encrypted_B = key.encrypt(bytes(userPass_Var.get(), 'utf-8'))
    encrypted_C = key.encrypt(bytes(remove_http, 'utf-8'))
    en_file =appdata_path+"\encrypted.dat"
    if os.path.exists((appdata_path +"\encrypted.dat")):
        os.remove(en_file)
    file1 = open(en_file,"wb")
    L = [encrypted_A,encrypted_B,encrypted_C]
    file1.write(encrypted_A)
    file1.write(b"\n")
    file1.write(encrypted_B)
    file1.write(b"\n")
    file1.write(encrypted_C)
    win32api.SetFileAttributes(en_file,win32con.FILE_ATTRIBUTE_HIDDEN)
    file1.close()
    first_Time_check = False
    messagebox.showinfo("Successful", "Your LogIn Information\nSaved Successfully")
    #print("Encryption successfull")

#clear all input field
def clear_field_fun ():
    fake_input_f_out.focus()
    userId_Var.set("Hint: my_username")
    userPass_Var.set("Eneter Password Here")
    userUrl_Var.set("Hint: 10.254.254.24/0/up/")
    uname_input.config(fg = 'grey')
    upass_input.config(fg = 'grey')
    uUrl_input.config(fg = 'grey')
    upass_input.config(show="")

#delete saved login info file on button click
def reset_login_info_button_fun ():
    en_file =appdata_path+"\encrypted.dat"
    if os.path.exists((appdata_path +"\encrypted.dat")):
        os.remove(en_file)
    messagebox.showinfo("Successful", "Your LogIn Information\nReset Successfully")
    clear_field_fun()

#main login function that try to login and fatch user details

def main_login_fun (u):
    global main_url,btn_st,failled_count
    username=userId_Var.get()
    password=userPass_Var.get()
    main_url=u
    fake_input_f_out.focus()
    #print("Attempting to login..")
    if failled_count < 5:
        #print(failled_count)
        payload = {'user': username,
                'pass': password,
                'login': 'Login'}
        try:
            requests.post(main_url, data=payload)
            r = requests.get(main_url).text
            soup = BeautifulSoup(r, "lxml")
            soup = soup.find('table', attrs={'id': 'thesmalltable'})
            try:
                rows = soup.find_all('tr')
            except AttributeError :
                failled_count = failled_count+1
                Logout_payload = {'logout': 'Logout'}
                requests.post(main_url, data=Logout_payload)
                main_login_fun(main_url)
            # show only name, client id, package and expiry date
            soup = soup.find('table', attrs={'id': 'thesmalltable'})
            name = rows[0].find_all('td')[1].text
            show_username.set(name)
            address = rows[1].find_all('td')[1].text
            show_user_address.set(address)
            client_id = rows[2].find_all('td')[1].text
            show_user_client_ID.set(client_id)
            package = rows[3].find_all('td')[1].text
            show_user_package.set(package)
            expiry = rows[4].find_all('td')[1].text
            show_user_expiry_date.set(expiry)
            email_id = rows[5].find_all('td')[1].text
            show_user_email.set(email_id)
            #print("Logged In")
            login_button.place(x=1200,y=4500)
            logout_button.place(x=120,y=450)
            #user address
            N_A = show_user_address.get()
            add_Text_Box.configure(state='normal')
            add_Text_Box.delete("1.9","end")
            add_Text_Box.insert(END,N_A)
            add_Text_Box.configure(state='disabled')
            #user client Id
            N_A2 = show_user_client_ID.get()
            client_Text_Box.configure(state='normal')
            client_Text_Box.delete("1.11","end")
            client_Text_Box.insert(END,N_A2)
            client_Text_Box.configure(state='disabled')
            #user package
            N_A3 = show_user_package.get()
            package_Text_Box.configure(state='normal')
            package_Text_Box.delete("1.9","end")
            package_Text_Box.insert(END,N_A3)
            package_Text_Box.configure(state='disabled')
            #user Expiry Date
            N_A4 = show_user_expiry_date.get()
            expiry_date_Text_Box.configure(state='normal')
            expiry_date_Text_Box.delete("1.13","end")
            expiry_date_Text_Box.insert(END,N_A4)
            expiry_date_Text_Box.configure(state='disabled')
            #Email Id
            N_A5 =show_user_email.get()
            email_Text_Box.configure(state='normal')
            email_Text_Box.delete("1.8","end")
            if N_A5 == "n/a" :
                N_A5 = "Email ID Not Registered"
            email_Text_Box.insert(END,N_A5)
            email_Text_Box.tag_add("Email ID Not Registered", "1.8", "1.31")
            email_Text_Box.tag_config("Email ID Not Registered",foreground="orangered2")
            email_Text_Box.configure(state='disabled')
            Big_user_name.config(fg="green")
            Save_Info_Button.config(state="normal")
            btn_st ="normal"
            save_login_info()
            #switch_wellcome_label(1)
        except AttributeError:
            failled_count = failled_count+1
            #pass
        except Exception as a:
            failled_count = 0
            messagebox.showerror("Login Failed", "Login To Alliance Broadband Failed\nPlease Check Your User Id, Password, & URL\nIf You Still Get This Error Try To Login Manually")
            #print("Could not connect to alliance server")
    else:
        failled_count = 0
        messagebox.showerror("Login Failed", "Login To Alliance Broadband Failed\nPlease Check Your User Id, Password, & URL\nIf You Still Get This Error Try To Login Manually")

#logout function
def main_logout_fun ():
    global failled_count
    failled_count = 0
    #print("Attempting to Logout")
    payload = {'logout': 'Logout'}
    fake_input_f_out.focus()
    try:
        requests.post(main_url, data=payload)
        #print("Logged Out")
        login_button.place(x=125,y=450)
        logout_button.place(x=1000,y=4500)

        #address text box clear and old state
        add_Text_Box.configure(state='normal')
        add_Text_Box.delete("1.9",END)
        add_Text_Box.insert(END,"Login First")
        add_Text_Box.tag_add("Login First", "1.9", "1.20")
        add_Text_Box.tag_config("Login First",foreground="IndianRed2")
        add_Text_Box.configure(state='disabled')

        #client id text box clear and old state
        client_Text_Box.configure(state='normal')
        client_Text_Box.delete("1.11",END)
        client_Text_Box.insert(END,"Login First")
        client_Text_Box.tag_add("Login First", "1.11", "1.22")
        client_Text_Box.tag_config("Login First",foreground="IndianRed2")
        client_Text_Box.configure(state='disabled')

        #Package text box clear and old state
        package_Text_Box.configure(state='normal')
        package_Text_Box.delete("1.9",END)
        package_Text_Box.insert(END,"Login First")
        package_Text_Box.tag_add("Login First", "1.9", "1.20")
        package_Text_Box.tag_config("Login First",foreground="IndianRed2")
        package_Text_Box.configure(state='disabled')

        #Expiry Date text box clear and old state
        expiry_date_Text_Box.configure(state='normal')
        expiry_date_Text_Box.delete("1.13",END)
        expiry_date_Text_Box.insert(END,"Login First")
        expiry_date_Text_Box.tag_add("Login First", "1.13", "1.24")
        expiry_date_Text_Box.tag_config("Login First",foreground="IndianRed2")
        expiry_date_Text_Box.configure(state='disabled')

        #email text box clear and old state
        email_Text_Box.configure(state='normal')
        email_Text_Box.delete("1.8",END)
        email_Text_Box.insert(END,"Login First")
        email_Text_Box.tag_add("Login First", "1.8", "1.19")
        email_Text_Box.tag_config("Login First",foreground="IndianRed2")
        email_Text_Box.configure(state='disabled')
        show_username.set("User Not Logged In")
        Big_user_name.config(fg="IndianRed1")
        switch_wellcome_label(2)
    except:
        messagebox.showerror("Logout Failed", "Logout To Alliance Broadband Failed\nPlease Check Your URL & Internet Connection\nIf You Still Get This Error Try To Logout Manually")
        #print("Could not connect to alliance server")


#check for all login info field fills or not and also check for correct info put or not
def checking_credential_Login_Info():
    global failled_count
    #check if any field fill or not
    regex = re.compile('_')
    string = userUrl_Var.get()
    failled_count = 0
    #print("checking_credential_Login_Info")
    if userId_Var.get() == 'Hint: my_username' or userPass_Var.get() == 'Eneter Password Here' or userUrl_Var.get() == 'Hint: 10.254.254.24/0/up/':
        messagebox.showwarning("Warning", "Please Fillups \nAll Required Filleds")
    elif (regex.search(userId_Var.get()) == None):
        messagebox.showerror("Error", "Please Input Valid \nAlliance User ID")

    elif validators.url(string) != True:
        N_url = "http://"+string
        main_login_fun(N_url)

    elif validators.url(string) == True:
        if (string.find('https://') != -1):
            remove_https = string[8:]
            N_url = "http://"+remove_https
            main_login_fun(N_url)
    	    #print ("Contains given substring ")
        elif (string.find('http://') != -1):
            main_login_fun(string)

#def menu_open_or_close ():


#to show scrool text
deli = 550
#v ="False"
def shif():
    shif.msg = shif.msg[1:] + shif.msg[0]
    scrollText.set(shif.msg)
    if v == "True":
        root.after(deli, shif)
    #print("Hi")
shif.msg = emoji.emojize("                                                                    \u260e24/7 Customer care:  033-71002000     \U0001f4f1Toll free:  1800 1200 300     \U0001f4e7Email:  abspl@alliancebroadband.co.in")




# setting switch function:
def switch():
    global btnState,v
    if btnState is True:
        # create animated Navbar closing:
        for x in range(201):
            navRoot.place(x=-x, y=0)
            topFrame.update()

        # resetting widget colors:
        v = "True"
        shif()
        homeLabel.config(bg=color["orange"])
        topFrame.config(bg=color["orange"])
        scrollText_Label.config(bg="lightgoldenrodyellow")
        field_reset_Button.config(state="normal")
        #Enable Home Frame
        brandLabel.config(bg="white")
        uname_label.config(bg="white", fg="green")
        upass_label.config(bg="white", fg="green")
        uUrl_label.config(bg="white", fg="green")
        username_wellcome_label_When_looged_out_frame.config(bg="white", fg="green")
        username_wellcome_label.config(bg="white", fg="green")
        wellcome_label.config(bg="white", fg="green")
        uname_input.configure(bg="white",state='normal')
        upass_input.configure(bg="white",state='normal')
        uUrl_input.configure(bg="white",state='normal')
        login_button.configure(state='normal')
        logout_button.configure(state='normal')
        eye_open_button.configure(state='normal')


        #Profile Frame Enable
        brandLabel2.config(bg="white")
        add_Text_Box.config(bg="white")
        client_Text_Box.config(bg="white")
        package_Text_Box.config(bg="white")
        expiry_date_Text_Box.config(bg="white")
        email_Text_Box.config(bg="white")
        Big_user_name.config(bg="white")

        #Other Frame Enable
        Save_Info_msg_Label.config(bg="white",fg="cornflower blue")
        Save_Info_msg_Label2.config(bg="white",fg="red")
        reset_msg_Label.config(bg="white",fg="cornflower blue")
        payment_msg_Label.config(bg="white",fg="cornflower blue")
        if btn_st == "normal":
            Save_Info_Button.configure(state='normal')
        reset_Button.configure(state='normal')
        payment_Button.configure(state='normal')

        #About Frame Enable

        About_label_hello.config(bg="floral white",fg="lightpink4")
        About_label.config(bg="floral white",fg="lightpink4")
        About_label_D_IN.config(bg="floral white",fg="plum4")
        contct_label.config(bg="white",fg="snow4")
        github_B.configure(state='normal')
        fb_B.configure(state='normal')
        Hackerrank_B.configure(state='normal')
        all_Button.configure(bg="floral white",fg="lightpink4",state='normal')



#gainsboro
#DarkSeaGreen3

        #root.config(bg="gray17")
        # turning button OFF:
        btnState = False
    else:
        # make root dim:
        v = "False"
        homeLabel.config(bg="#F2913D")
        topFrame.config(bg="#F2913D")
        scrollText_Label.config(bg="#fdfded")
        field_reset_Button.config(state="disable")

        #Disable Home Frame

        #uname_label.config(bg=color["nero"], fg="#5F5A33")
        brandLabel.config(bg="gainsboro")
        uname_label.config(bg="gainsboro", fg="DarkSeaGreen3")
        upass_label.config(bg="gainsboro", fg="DarkSeaGreen3")
        uUrl_label.config(bg="gainsboro", fg="DarkSeaGreen3")
        username_wellcome_label_When_looged_out_frame.config(bg="gainsboro", fg="DarkSeaGreen3")
        username_wellcome_label.config(bg="gainsboro", fg="DarkSeaGreen3")
        wellcome_label.config(bg="gainsboro", fg="DarkSeaGreen3")
        uname_input.configure(bg="gainsboro",state='disable')
        upass_input.configure(bg="gainsboro",state='disable')
        uUrl_input.configure(bg="gainsboro",state='disable')
        login_button.configure(state='disable')
        logout_button.configure(state='disable')
        #uname_input.configure(state='disable')
        if userPass_Var.get() != 'Eneter Password Here':
            upass_input.config(show="*")
            eye_close_button.place(x=1000,y=1000)
            eye_open_button.place(x=260,y=336)
        eye_open_button.configure(state='disable')


        #Profile Frame Disbale
        brandLabel2.config(bg="gainsboro")
        add_Text_Box.config(bg="gainsboro")
        client_Text_Box.config(bg="gainsboro")
        package_Text_Box.config(bg="gainsboro")
        expiry_date_Text_Box.config(bg="gainsboro")
        email_Text_Box.config(bg="gainsboro")
        Big_user_name.config(bg="gainsboro")

        #Other Frame Disbale
        Save_Info_msg_Label.config(bg="gainsboro",fg="deepskyblue3")
        Save_Info_msg_Label2.config(bg="gainsboro",fg="#F75766")
        reset_msg_Label.config(bg="gainsboro",fg="deepskyblue3")
        payment_msg_Label.config(bg="gainsboro",fg="deepskyblue3")
        Save_Info_Button.configure(state='disable')
        reset_Button.configure(state='disable')
        payment_Button.configure(state='disable')


        #About Frame Disbale

        About_label_hello.config(bg="gainsboro",fg="light slate gray")
        About_label.config(bg="gainsboro",fg="light slate gray")
        About_label_D_IN.config(bg="gainsboro",fg="light slate gray")
        contct_label.config(bg="gainsboro",fg="light slate gray")
        github_B.configure(state='disable')
        fb_B.configure(state='disable')
        Hackerrank_B.configure(state='disable')
        all_Button.configure(bg="gainsboro",fg="light slate gray",state='disable')

#F75766
        #root.config(bg=color["nero"])

        # created animated Navbar opening:
        for x in range(-200, 0):
            navRoot.place(x=x, y=0)
            topFrame.update()

        # turing button ON:
        btnState = True

# top Navigation bar:
topFrame = Frame(root, bg=color["orange"])
topFrame.pack(side="top", fill=X)

# Header label text:
homeLabel = Label(topFrame, text="HR", font=("Modern No. 20", 13), bg=color["orange"], fg="gray17", height=2, padx=20)
homeLabel.pack(side="right")
               #,anchor="ne")


#print ("Current date and time : ")
#print (now.strftime("%Y-%m-%d %H:%M:%S"))

#function for clock

def tic():
    homeLabel['text'] = time.strftime('%I:%M\n%d.%m.%y')

tic()

def tac():
    tic()
    homeLabel.after(1000, tac)

tac()

scrollText_Label = Label(root, bg ="lightgoldenrodyellow", font = ("Segoe UI Emoji",10),textvariable=scrollText, height=1 )
scrollText_Label.place(x=0,y=46)



#Segoe UI Emoji


Home_Frame = Frame(root,bg="gray17")
Profile_Frame = Frame(root,bg="gray17")
About_Frame = Frame(root,bg="gray17")
other_Frame = Frame(root,bg="gray17")

def switch_home_frame():
    Profile_Frame.place(x=1005,y=8000)
    About_Frame.place(x=1005,y=8000)
    other_Frame.place(x=1005,y=8000)
    Home_Frame.place(x=37,y=72)
    field_reset_Button.place(x=358,y=556)
    switch()

def switch_profile_frame():
    Home_Frame.place(x=1005,y=8000)
    About_Frame.place(x=1005,y=8000)
    other_Frame.place(x=1005,y=8000)
    Profile_Frame.place(x=37,y=72)
    field_reset_Button.place(x=1005,y=8000)
    switch()

def switch_about_frame():
    Home_Frame.place(x=1005,y=8000)
    Profile_Frame.place(x=1005,y=8000)
    other_Frame.place(x=1005,y=8000)
    About_Frame.place(x=18,y=80)
    field_reset_Button.place(x=1005,y=8000)
    switch()

def switch_other_frame():
    Home_Frame.place(x=1005,y=8000)
    Profile_Frame.place(x=1005,y=8000)
    About_Frame.place(x=1005,y=8000)
    other_Frame.place(x=35,y=72)
    field_reset_Button.place(x=1005,y=8000)
    switch()

# Main label text:


Home_Frame.place(x=37,y=72)
#Home_Frame.place(x=37,y=64)

brandLabel = Label(Home_Frame, image=logoIcon, bg="white", fg="green")
brandLabel.pack()
Label(Home_Frame, text = "    ",font="BahnschriftLight 4",bg="gray17").pack()




wellframe =Frame(Home_Frame,bg="grey17")
wellframe.pack(side=TOP)




username_wellcome_label = Label(wellframe,text="Wellcome", font=('Harlow Solid Italic',17), bg="white", fg="green")
username_wellcome_label.pack()
Label(wellframe, text = "    ",font="BahnschriftLight 2",bg="gray17").pack()
wellcome_label = Label(wellframe,textvariable= show_username, font=('Berlin Sans FB',27), bg="white", fg="green")
wellcome_label.pack()

wellframe_fake =Frame(Home_Frame,bg="grey17")
#wellframe_fake.place(x=0,y=108)

username_wellcome_label_fake=Label(wellframe_fake,text="                                                   ", font=('Harlow Solid Italic',17), bg="grey17", fg="green").pack()
username_wellcome_label_fake2=Label(wellframe_fake,text="                                                  ", font=('Harlow Solid Italic',17), bg="grey17", fg="green").pack()
wellcome_label_fake=Label(wellframe_fake,text="                                                            ", font=('Harlow Solid Italic',23), bg="grey17", fg="green").pack()

When_looged_out_frame = Frame(Home_Frame)
#When_looged_out_frame.place(x=76,y=136)
username_wellcome_label_When_looged_out_frame=Label(When_looged_out_frame,text="Wellcome", font=('Harlow Solid Italic',30), bg="white", fg="green")
username_wellcome_label_When_looged_out_frame.pack()


def switch_wellcome_label(s):
    #print("def")
    if s == 1:  #when user logged in
        #print("1")
        #main_login_fun ()
        wellframe_fake.place(x=1000,y=1000)
        When_looged_out_frame.place(x=1000,y=1000)

    if s == 2: #when user logged out
        #print("2")
        wellframe_fake.place(x=0,y=108)
        When_looged_out_frame.place(x=76,y=136)

switch_wellcome_label(2)

Label(wellframe, text = "    ",font="BahnschriftLight 15",bg="gray17").pack()


#Entry Box Clear AndHide Password
def on_uname_input_click(event):
    if userId_Var.get() == 'Hint: my_username':
       uname_input.delete(0, "end") # delete all the text in the entry
       uname_input.insert(0, '') #Insert blank for user input
       uname_input.config(fg = 'black')
def on_uname_input_focusout(event):
    if first_Time_check == False and userId_Var.get () != 'Hint: my_username':
        uname_input.config(fg = 'black')
    if uname_input.get() == '':
        userId_Var.set('Hint: my_username')
        uname_input.config(fg = 'grey')

def on_uUrl_input_click(event):
    if userUrl_Var.get() == 'Hint: 10.254.254.24/0/up/':
       uUrl_input.delete(0, "end") # delete all the text in the entry
       uUrl_input.insert(0, '') #Insert blank for user input
       uUrl_input.config(fg = 'black')
def on_uUrl_input_focusout(event):
    if first_Time_check == False and userUrl_Var.get() != ("Hint: 10.254.254.24/0/up/"):
        uUrl_input.config(fg = 'black')
    if uUrl_input.get() == '':
        userUrl_Var.set("Hint: 10.254.254.24/0/up/")
        uUrl_input.config(fg = 'grey')

def on_upass_input_click(event):
    if userPass_Var.get() == 'Eneter Password Here':
        upass_input.delete(0, "end") # delete all the text in the entry
        upass_input.insert(0, '') #Insert blank for user input
        upass_input.config(fg = 'black',show="*")


def on_upass_input_focusout(event):
    if upass_input.get() == '':
        userPass_Var.set("Eneter Password Here")
        upass_input.config(fg = 'grey',show="")
    if userPass_Var.get() != 'Eneter Password Here':
        upass_input.config(fg = 'black',show="*")
        eye_close_button.place(x=1000,y=1000)
        eye_open_button.place(x=260,y=336)

def function_eye_open_button ():
    if userPass_Var.get() != 'Eneter Password Here':
        upass_input.config(show="")
        eye_open_button.place(x=1000,y=1000)
        eye_close_button.place(x=260,y=336)

def function_eye_close_button ():
    if userPass_Var.get() != 'Eneter Password Here':
        upass_input.config(show="*")
        eye_close_button.place(x=1000,y=1000)
        eye_open_button.place(x=260,y=336)



#Frames Configarations
fake_input_f_out = Entry(Home_Frame)
fake_input_f_out.place(x=1000,y=1000)

uname_label = Label(Home_Frame,text="Enter Alliance User ID",font=("Copperplate Gothic Bold",11),bg="white", fg="green")
uname_label.pack()

Label(Home_Frame, text = "    ",font="BahnschriftLight 2",bg="gray17").pack()

uname_input = Entry(Home_Frame,textvariable= userId_Var,font=("Comic Sans MS",11),fg = 'grey',bd=3)
uname_input.bind('<FocusIn>', on_uname_input_click)
uname_input.bind('<FocusOut>', on_uname_input_focusout)
uname_input.pack()

Label(Home_Frame, text = "    ",font="BahnschriftLight 6",bg="gray17").pack()

upass_label = Label(Home_Frame,text="Enter Alliance Password",font=("Copperplate Gothic Bold",11),bg="white", fg="green")
upass_label.pack()

eye_close_button = Button(Home_Frame, image=eye_close, bd=2, padx=10,command=function_eye_close_button)
#eye_close_button.place(x=260,y=336)

eye_open_button = Button(Home_Frame, image=eye_open, bd=2, padx=10,command=function_eye_open_button)
eye_open_button.place(x=260,y=336)


Label(Home_Frame, text = "    ",font="BahnschriftLight 2",bg="gray17").pack()

upass_input = Entry(Home_Frame,textvariable= userPass_Var,font=("Comic Sans MS",11),bd=3,fg = 'grey')
upass_input.bind('<FocusIn>', on_upass_input_click)
upass_input.bind('<FocusOut>', on_upass_input_focusout)
upass_input.pack()

Label(Home_Frame, text = "    ",font="BahnschriftLight 6",bg="gray17").pack()

uUrl_label = Label(Home_Frame,text="Enter Alliance Login URL",font=("Copperplate Gothic Bold",11),bg="white", fg="green")
uUrl_label.pack()

Label(Home_Frame, text = "    ",font="BahnschriftLight 2",bg="gray17").pack()

uUrl_input = Entry(Home_Frame,textvariable= userUrl_Var,font=("Comic Sans MS",11),bd=3,fg = 'grey',width=21)
uUrl_input.bind('<FocusIn>', on_uUrl_input_click)
uUrl_input.bind('<FocusOut>', on_uUrl_input_focusout)
uUrl_input.pack()




fake_label_for_button_Space = Label(Home_Frame,text="        \n \n   ",font=("rockwell",50),bg="grey17").pack()

login_button = Button(Home_Frame,text="Login",font=("rockwell",11),command = checking_credential_Login_Info,bd = 6,padx = 6)
login_button.place(x=125,y=450)
logout_button = Button(Home_Frame,text="Logout",font=("rockwell",11),command = main_logout_fun,bd = 6,padx = 6)
#logout_button.place(x=120,y=450)


#Profile_Frame.place(x=37,y=68)

brandLabel2 = Label(Profile_Frame, image=logoIcon, bg="white", fg="green")
brandLabel2.pack()
Label(Profile_Frame, text = "    ",font="BahnschriftLight 6",bg="gray17").pack()

Big_user_name = Label(Profile_Frame,textvariable= show_username, font=('Berlin Sans FB',27), bg="white", fg="IndianRed1")
Big_user_name.pack()

Label(Profile_Frame, text = "    ",font="BahnschriftLight 6",bg="gray17").pack()

add_Text_Box = Text (Profile_Frame,bg="white",font=("Maiandra GD",14),fg="cyan4",width=25,height=5,bd=3)
add_Text_Box.insert(END,"Address: ")
add_Text_Box.tag_add("Address: ", "1.0", "1.8")
add_Text_Box.tag_config("Address: ",font=("Copperplate Gothic Bold",12),foreground="light slate blue")
add_Text_Box.insert(END,"Login First")
add_Text_Box.tag_add("Login First", "1.9", "1.20")
add_Text_Box.tag_config("Login First",foreground="IndianRed2")
add_Text_Box.configure(state='disabled')
add_Text_Box.pack()
#"light slate blue"
#Cooper Black
Label(Profile_Frame, text = "    ",font="BahnschriftLight 3",bg="gray17").pack()

client_Text_Box = Text (Profile_Frame,bg="white",font=("Maiandra GD",14),fg="cyan4",width=25,height=1,bd=3)
client_Text_Box.insert(END,"Client ID: ")
client_Text_Box.tag_add("Client ID: ", "1.0", "1.10")
client_Text_Box.tag_config("Client ID: ",font=("Copperplate Gothic Bold",12),foreground="light slate blue")
client_Text_Box.insert(END,"Login First")
client_Text_Box.tag_add("Login First", "1.11", "1.22")
client_Text_Box.tag_config("Login First",foreground="IndianRed2")
client_Text_Box.configure(state='disabled')
client_Text_Box.pack()

Label(Profile_Frame, text = "    ",font="BahnschriftLight 4",bg="gray17").pack()

package_Text_Box = Text (Profile_Frame,bg="white",font=("Maiandra GD",14),fg="cyan4",width=25,height=1,bd=3)
package_Text_Box.insert(END,"Package: ")
package_Text_Box.tag_add("Package: ", "1.0", "1.9")
package_Text_Box.tag_config("Package: ",font=("Copperplate Gothic Bold",12),foreground="light slate blue")
package_Text_Box.insert(END,"Login First")
package_Text_Box.tag_add("Login First", "1.9", "1.20")
package_Text_Box.tag_config("Login First",foreground="IndianRed2")
package_Text_Box.configure(state='disabled')
package_Text_Box.pack()

Label(Profile_Frame, text = "    ",font="BahnschriftLight 3",bg="gray17").pack()

expiry_date_Text_Box = Text (Profile_Frame,bg="white",font=("Maiandra GD",14),fg="cyan4",width=25,height=1,bd=3)
expiry_date_Text_Box.insert(END,"Expiry Date: ")
expiry_date_Text_Box.tag_add("Expiry Date: ", "1.0", "1.13")
expiry_date_Text_Box.tag_config("Expiry Date: ",font=("Copperplate Gothic Bold",12),foreground="light slate blue")
expiry_date_Text_Box.insert(END,"Login First")
expiry_date_Text_Box.tag_add("Login First", "1.13", "1.24")
expiry_date_Text_Box.tag_config("Login First",foreground="IndianRed2")
expiry_date_Text_Box.configure(state='disabled')
expiry_date_Text_Box.pack()

Label(Profile_Frame, text = "    ",font="BahnschriftLight 3",bg="gray17").pack()

email_Text_Box = Text (Profile_Frame,bg="white",font=("Maiandra GD",14),fg="cyan4",width=25,height=1.5,bd=3)
email_Text_Box.insert(END,"E-mail: ")
email_Text_Box.tag_add("E-mail: ", "1.0", "1.8")
email_Text_Box.tag_config("E-mail: ",font=("Copperplate Gothic Bold",12),foreground="light slate blue")
email_Text_Box.insert(END,"Login First")
email_Text_Box.tag_add("Login First", "1.8", "1.19")
email_Text_Box.tag_config("Login First",foreground="IndianRed2")
email_Text_Box.configure(state='disabled')
email_Text_Box.pack()



def exit_fun ():
    ans = messagebox.askyesno("Exit", "Are You Sure,\nYou want to Exit IP Connect?")
    if ans == True:
        root.destroy()





field_reset_Button = Button(root,image=f_reset_B, bd=2, padx=10,command=clear_field_fun)
field_reset_Button.place(x=358,y=556)
CreateToolTip(field_reset_Button, text = "Clear All Entry Fields")
#dark turquoise

#Other Page
Save_Info_msg_Label = Label(other_Frame, text = "If You Want To Save\nLogin Info For Future Login\nPlease Click On Bellow Button",font=("Eras Demi ITC",14),bg="white",fg="cornflower blue")
Save_Info_msg_Label.pack()

Label(other_Frame, text = "    ",font="BahnschriftLight 1",bg="gray17").pack()

Save_Info_msg_Label2 = Label(other_Frame, text = "**This Button Only Work After A Successful Login**",font=("Arial Rounded MT Bold",10),bg="white",fg="red")
Save_Info_msg_Label2.pack()

Label(other_Frame, text = "    ",font="BahnschriftLight 3",bg="gray17").pack()

Save_Info_Button = Button(other_Frame,image=save_B, bd=2, padx=10,command=save_login_info_button_fun)
Save_Info_Button.pack()
Save_Info_Button.config(state='disabled')
btn_st="disabled"

Label(other_Frame, text = "    ",font="BahnschriftLight 6",bg="gray17").pack()

reset_msg_Label = Label(other_Frame, text = "If You Want To Delete\nYour Saved Login Info Data\nPlease Click On Bellow Button",font=("Eras Demi ITC",14),bg="white",fg="cornflower blue")
reset_msg_Label.pack()

Label(other_Frame, text = "    ",font="BahnschriftLight 3",bg="gray17").pack()

reset_Button = Button(other_Frame, image=reset_B, bd=2, padx=10,command=reset_login_info_button_fun)
reset_Button.pack()

Label(other_Frame, text = "    ",font="BahnschriftLight 6",bg="gray17").pack()



payment_msg_Label = Label(other_Frame, text = "If You Want To Recharge\nYour Alliance Broadband\nPlease Click On Bellow Button",font=("Eras Demi ITC",14),bg="white",fg="cornflower blue")
payment_msg_Label.pack()
Label(other_Frame, text = "    ",font="BahnschriftLight 3",bg="gray17").pack()
payment_Button = Button(other_Frame,text ="Recharge", image=pay_B, bd=2, padx=10,command=lambda: webbrowser.open_new_tab("https://pay2abs.alliancebroadband.in"))
payment_Button.pack()
CreateToolTip(payment_Button, text = "It's Open Alliance Broadband \nOnline Payment Page")


def on_enter(ev):
    all_Button.config(fg="dodger blue")
def on_leave(ev):
    all_Button.config(fg="lightpink4")
#About Page

#Alliance Broadband.This Program Or Software Is Completely Unofficial



About_label_hello = Label(About_Frame, text = "Hello World !!",font=("Lucida Calligraphy",15),bg="floral white",fg="lightpink4")
About_label_hello.pack()
About_label = Label(About_Frame, text = "\nThis Program Was Written In Python\nLanguage 3.9.0 With Tkinter GUI And\nOther Modules Is pywin32, bs4, getpass,\nwebbrowser, validators, requests,\n& cryptography. This Program Save\nUser Login Information With A Privet\nKey Encryption. This Program Is\nInspired Form IP Connector By\nAlliance Broadband. This Program Or\nSoftware Is Completely Unofficial.",font=("Lucida Calligraphy",13),bg="floral white",fg="lightpink4")
About_label.pack()

Label(About_Frame, text = "    ",font="BahnschriftLight 5",bg="gray17").pack()

About_label_D_IN = Label(About_Frame, text = "IP Connect v2.0 Developed By\nHrishikesh Patra",font=("Lucida Calligraphy",16),bg="floral white",fg="plum4")
About_label_D_IN.pack()

all_Button =Button(About_Frame,text="Alliance Broadband.",bd=0,font=("Lucida Calligraphy",12),bg="floral white",fg="lightpink4", command=lambda: webbrowser.open_new_tab("http://alliancebroadband.co.in"))
all_Button.bind("<Enter>", on_enter)
all_Button.bind("<Leave>", on_leave)
all_Button.place(x=4,y=238)


Label(About_Frame, text = "    ",font="BahnschriftLight 7",bg="gray17").pack()

contct_label = Label(About_Frame, text = "Contact With Me :-",font="forte 15",bg="white",fg="snow4")
contct_label.pack()

Label(About_Frame, text = "    ",font="BahnschriftLight 5",bg="gray17").pack()

Label(About_Frame, text = "                                       ",font="BahnschriftLight 5",bg="gray17").pack(side=RIGHT)
Hackerrank_B = Button(About_Frame,image=Hackerrank_Icon, bd=4, padx=10,command=lambda: webbrowser.open_new_tab("https://www.hackerrank.com/Hrishikesh7665"))
Hackerrank_B.pack(side=RIGHT)
Label(About_Frame, text = "        ",font="BahnschriftLight 5",bg="gray17").pack(side=RIGHT)

fb_B = Button(About_Frame,image=fb_Icon, bd=4, padx=10,command=lambda: webbrowser.open_new_tab("https://www.facebook.com/Isjtijlfti.patra"))
fb_B.pack(side=RIGHT)

Label(About_Frame, text = "        ",font="BahnschriftLight 5",bg="gray17").pack(side=RIGHT)

github_B = Button(About_Frame,image=github_Icon, bd=4, padx=10,command=lambda: webbrowser.open_new_tab("https://github.com/Hrishikesh7665"))
github_B.pack(side=RIGHT)



# Navbar button:
navbarBtn = Button(topFrame, image=navIcon, bg=color["orange"], activebackground=color["orange"], bd=0, padx=20, command=switch)
navbarBtn.place(x=10, y=10)

# setting Navbar frame:
navRoot = Frame(root, bg="gray38", height=1000, width=200)
navRoot.place(x=-200, y=0)
Label(navRoot, font="Bahnschrift 15", bg="#ffae60", fg="black", height=2, width=300, padx=20).place(x=0, y=0)



NavB1 = Button(navRoot, text="  Home",image=home_icon,compound = LEFT, font="BahnschriftLight 15", bg="gray38", fg="gold2", activebackground="gray23", activeforeground="darkseagreen1", bd=0,command=switch_home_frame)
NavB1.place(x=25, y=80)
NavB2 = Button(navRoot, text="  Profile",image=profile_icon,compound = LEFT, font="BahnschriftLight 15", bg="gray38", fg="gold2", activebackground="gray23", activeforeground="darkseagreen1", bd=0,command=switch_profile_frame)
NavB2.place(x=25, y=120)
NavB3 = Button(navRoot, text="  Others", image=others_icon,compound = LEFT, font="BahnschriftLight 15", bg="gray38", fg="gold2", activebackground="gray23", activeforeground="darkseagreen1", bd=0,command=switch_other_frame)
NavB3.place(x=25, y=160)
NavB4 = Button(navRoot, text="  About",image=about_icon,compound = LEFT, font="BahnschriftLight 15", bg="gray38", fg="gold2", activebackground="gray23", activeforeground="darkseagreen1", bd=0,command=switch_about_frame)
NavB4.place(x=25, y=200)
NavB5 = Button(navRoot, text="  Exit",image=exit_icon,compound = LEFT, font="BahnschriftLight 15", bg="gray38", fg="gold2", activebackground="firebrick1", activeforeground="white", bd=0,command=exit_fun)
NavB5.place(x=25, y=240)
#Button(navRoot, text="Feedback", font="BahnschriftLight 15", bg="gray17", fg=color["orange"], activebackground="gray17", activeforeground="green", bd=0).place(x=25, y=240)
#Button(navRoot, text="  Exit",image=exit_icon,compound = LEFT, font="BahnschriftLight 15", bg="gray38", fg="gold2", activebackground="gray23", activeforeground="darkseagreen1", bd=0).place(x=25, y=240)
Label(navRoot, text="Devolpoed By Hrishikesh Patra",compound = LEFT,font="BahnschriftLight 10",bg="gray38", fg="old lace",bd=0).place(x=9, y=560)# Navbar Close Button:


closeBtn = Button(navRoot, image=closeIcon, bg="#ffae60", activebackground="#ffc966", bd=0, command=switch)
closeBtn.place(x=150, y=10)




root.wm_protocol ("WM_DELETE_WINDOW",exit_fun )

shif()
check_login_file_avalability()
# window in mainloop:
root.mainloop()