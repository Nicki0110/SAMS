from tkinter import messagebox
import time
from tkinter import ttk, filedialog
from tkinter import *
import tkinter.messagebox as tkMessagebox
import sqlite3
from PIL import ImageTk
from tkinter import Tk
from tkinter import Label
from tkinter import colorchooser
from configparser import ConfigParser
import tkinter as tk
import re
import os
import datetime
import cv2
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ctypes
import os



def qr():
    root = Tk()
    root.geometry("1156x650+120+30")
    root.title("Student Management System")
    bgImage = ImageTk.PhotoImage(file='D:/dist - Copy/qrcode.png')
    bgLabel = Label(root, image=bgImage)
    bgLabel.pack()
    root.resizable(False, False)
    root.iconbitmap('D:/dist - Copy/logo.ico')

    def scan():
        log_path = 'D:/dist - Copy/database.csv'

        cap = cv2.VideoCapture(0)

        most_recent_access = {}
        time_between_logs = 5

        while True:
            ret, frame = cap.read()

            qr_info = decode(frame)

            if len(qr_info) > 0:
                qr = qr_info[0]

                data = qr.data
                rect = qr.rect
                polygon = qr.polygon

                cv2.putText(frame, data.decode(), (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                if data.decode() not in most_recent_access.keys() \
                        or most_recent_access[data.decode()] - time.time() > time_between_logs:
                    most_recent_access[data.decode()] = time.time()
                    with open(log_path, 'a') as f:
                        f.write('{},{},{}\n'.format(data.decode(), datetime.datetime.now(), 'Present'))
                        f.close()
                frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                                      (0, 255, 0), 5)

                frame = cv2.polylines(frame, [np.array(polygon)], True, (255, 0, 0), 5)



            cv2.imshow('webcam', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def loginbutton():
        root.destroy()
        main()

    qrcode = Button(root, text='TAP TO SCAN ID', width=23, height=1, font=('Barlow Light', 19, 'bold'), bg='#0A4016',
                           fg='white'
                           , activebackground='#0C4E1B', activeforeground='#A0F18D', cursor='hand2', bd=0,
                           command=scan)
    qrcode.place(x=400, y=530)

    LoginButton = Button(root, text='Proceed to Log In', font=('Barlow Bold', 10, 'bold', 'underline'), fg='white',
                         bg='#0A4016'
                         , activebackground='white', activeforeground='blue', cursor='hand2', bd=0, command=loginbutton)
    LoginButton.place(x=520, y=590)


    root.mainloop()
def main():

    def login():

        with sqlite3.connect('D://dist - Copy//attendance0.db') as db:
            c = db.cursor()
            find_user = ('select * from record where email = ? and pass = ?')
            c.execute(find_user, [(namew.get()),(passw.get())])
            result = c.fetchall()

        if result:
            messagebox.showinfo('Successful', 'Login Complete! ')
            login_window.destroy()
            homes()
        else:
            messagebox.showerror('Error','Please Sign Up')



    def signup_page():
        login_window.destroy()
        signup()



    def hide():
        closeye.config(file='D:/dist - Copy/closeye.png')
        passwordEntry.config(show='*')
        eyeButton.config(command=show)

    def show():
        closeye.config(file='D:/dist - Copy/openeye.png')
        passwordEntry.config(show='')
        eyeButton.config(command=hide)

    def qrcodewindow():
        login_window.destroy()
        qr()


    def email_enterleave(event):
        name = usernameEntry.get()
        if name =='':
                usernameEntry.insert(0,'Email')

    def email_enterenter(event):
        usernameEntry.delete(0,'end')

    def password_enterleave(event):
        passs = passwordEntry.get()
        if passs =='':
                passwordEntry.insert(0,'Password')

    def password_enterenter(event):
        passwordEntry.delete(0,'end')

    login_window = Tk()
    login_window.geometry('1156x650+120+30')
    login_window.resizable(0,0)
    login_window.title('Login Page')
    login_window.iconbitmap('D:/dist - Copy/logo.ico')

    bgImage = ImageTk.PhotoImage(file='D:/dist - Copy/logins.png')
    bgLabel = Label(login_window, image = bgImage)
    login_window.iconbitmap('D:/dist - Copy/logo.ico')
    bgLabel.grid(row=0, column=0)
    namew = StringVar()
    passw = StringVar()
    att = StringVar()

    def get_time():
        timevar=time.strftime("%H:%M:%S:%p:%a \n %x")
        clock.config(text=timevar)
        clock.after(200,get_time)

    clock = Label(login_window, font = ('Barlow Bold',17), bg= '#57D123',fg = '#0C4E1B')
    clock.place(x = 63,y = 38)
    get_time()



    usernameEntry=Entry(login_window,width=21, font = ('Barlow Medium',20),bd = 0,fg = '#0C4E1B',textvar=namew)
    usernameEntry.place(x=590,y=320)



    frame1=Frame(login_window,width=318,height=2,bg='#0C4E1B')
    frame1.place(x=590,y=353)



    passwordEntry=Entry(login_window,width=21, font = ('Barlow Medium',20),bd = 0,fg = '#0C4E1B',show = '*', textvar = passw)
    passwordEntry.place(x=590,y=420)
    passwordEntry.insert(0,'')

    passwordEntry.bind('<FocusIn>',password_enterenter)
    passwordEntry.bind('<FocusOut>',password_enterleave)
    frame2=Frame(login_window,width=318,height=2,bg='#0C4E1B')
    frame2.place(x=590,y=453)

    closeye=PhotoImage(file='D:/dist - Copy/closeye.png')
    eyeButton = Button(login_window,image=closeye,bd=0,bg='#C0FFBC',activebackground= '#0C4E1B',cursor='hand2',command=show)
    eyeButton.place(x=880,y=423)


    LoginButton=Button(login_window,text='Login',font=('Barlow Bold',16,'bold'),fg='white',bg= '#0C4E1B',activebackground= '#0C4E1B',activeforeground= '#A0F18D',cursor='hand2',bd=0,width=19
                   ,command=login)
    LoginButton.place(x=625,y=490)

    alreadyhaveButton=Label(login_window,text='Don"t have an account?',font=('Barlow Bold',10,'bold'),fg='#0C4E1B',bg= '#A0F18D')
    alreadyhaveButton.place(x=650,y=540)


    GotoLoginButton=Button(login_window,text='Sign Up',font=('Barlow Bold',8,'bold','underline'),fg='#0C4E1B',bg= '#A0F18D'
                    ,activebackground= 'white',activeforeground= 'blue',cursor='hand2',bd=0, command=signup_page)
    GotoLoginButton.place(x=810,y=540)


    login_window.mainloop()


def signup():
    def login_page():
        signup_window.destroy()
        main()

    def hide():
        closeye.config(file='D:/dist - Copy/closeye.png')
        passwordEntry.config(show='*')
        eyeButton.config(command=show)

    def show():
        closeye.config(file='D:/dist - Copy/openeye.png')
        passwordEntry.config(show='')
        eyeButton.config(command=hide)

    def hide1():
        closeye1.config(file='D:/dist - Copy/closeye2.png')
        confirmpassEntry.config(show='*')
        eyeButton2.config(command=show1)

    def show1():
        closeye1.config(file='D:/dist - Copy/openeye2.png')
        confirmpassEntry.config(show='')
        eyeButton2.config(command=hide1)

    def pass_enter(event):
        if passwordEntry.get() == '':
            passwordEntry.delete(0, END)

    def confirm_enter(event):
        if confirmpassEntry.get() == '':
            confirmpassEntry.delete(0, END)

    signup_window = Tk()
    signup_window.title('Signup Page')
    signup_window.geometry('1156x650+120+30')
    signup_window.resizable(False, False)
    background = ImageTk.PhotoImage(file='D:/dist - Copy/create_acc.png')
    signup_window.iconbitmap('D:/dist - Copy/logo.ico')

    bgLabel = Label(signup_window, image=background)
    bgLabel.grid(row=0, column=0)

    id1 = StringVar()
    gender = IntVar()
    email1 = StringVar()
    pass1 = StringVar()
    passa = StringVar()

    def get_time():
        timevar = time.strftime("%H:%M:%S:%p:%a \n %x")
        clock.config(text=timevar)
        clock.after(200, get_time)

    clock = Label(signup_window, font=('Barlow Bold', 18), bg='#57D123', fg='#0C4E1B')
    clock.place(x=87, y=25)
    get_time()

    def database():

        name = id1.get()
        gender2 = gender.get()
        email = email1.get()
        pass2 = pass1.get()
        pass3 = passa.get()

        conn = sqlite3.connect('D:/dist - Copy/attendance0.db')


        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS record (Email,Pass)')

        if email == '':
            messagebox.showinfo('Error', 'Please Enter a Valid Email! ')
        elif pass3 == '':
            messagebox.showinfo('Error', 'Please Enter a Valid Password! ')
        if email and pass3  == '':
            messagebox.showerror('Error', 'Please fill up the fields!')

        elif pass3 == pass2:
            cursor.execute('INSERT INTO record (Email, Pass) VALUES(?,?)', (email, pass2))
            conn.commit()
            messagebox.showinfo('Successful', 'Signup Complete! ')
            signup_window.destroy()
            main()
        else:
            messagebox.showinfo('Error', 'Password should be identical! ')


    emailEntry = Entry(signup_window, width=23, font=('Barlow Medium', 20),
                       fg='#0C4E1B', bg='white', textvar=email1).place(x=560, y=210)

    passwordEntry = Entry(signup_window, width=23, font=('Barlow Medium', 20),
                          fg='#0C4E1B',show = '*', bg='white', textvar=pass1)
    passwordEntry.place(x=560, y=320)
    passwordEntry.insert(0, '')
    passwordEntry.bind('<FocusIn>', pass_enter)

    confirmpassEntry = Entry(signup_window, width=23, font=('Barlow Medium', 20),
                             fg='#0C4E1B',show = '*', bg='white', textvar=passa)
    confirmpassEntry.place(x=560, y=440)
    confirmpassEntry.insert(0, '')
    confirmpassEntry.bind('<FocusIn>', confirm_enter)

    signupButton = Button(signup_window, text='Sign Up', font=('Barlow Bold', 16, 'bold'), fg='white', bg='#0C4E1B'
                          , activebackground='#0C4E1B', activeforeground='#A0F18D', cursor='hand2', bd=0, width=16,
                          command=database)
    signupButton.place(x=600, y=500)

    alreadyhaveButton = Label(signup_window, text='Do you have an account?', font=('Barlow Bold', 10, 'bold'),
                              fg='#0C4E1B', bg='#ACF39D')
    alreadyhaveButton.place(x=600, y=545)
    closeye = PhotoImage(file='closeye.png')
    closeye1 = PhotoImage(file= 'closeye2.png')
    eyeButton = Button(signup_window, image=closeye, bd=0, bg='#ACF39D', activebackground='#0C4E1B', cursor='hand2',
                       command=show)
    eyeButton.place(x=880, y=324)

    eyeButton2 = Button(signup_window, image=closeye1, bd=0, bg='#ACF39D', activebackground='#0C4E1B', cursor='hand2',
                        command=show1)
    eyeButton2.place(x=880, y=444)



    LoginButton = Button(signup_window, text='Log In', font=('Barlow Bold', 8, 'bold', 'underline'), fg='#0C4E1B',
                         bg='#ACF39D'
                         , activebackground='white', activeforeground='blue', cursor='hand2', bd=0, command=login_page)
    LoginButton.place(x=772, y=545)
    signup_window.mainloop()

def homes():
    home_window = Tk()
    home_window.title('Home Page')
    home_window.geometry('1156x650+120+30')
    home_window.resizable(False, False)
    background = ImageTk.PhotoImage(file='D:/dist - Copy/homes.png')
    home_window.iconbitmap('D:/dist - Copy/logo.ico')

    bgLabel = Label(home_window, image=background)
    bgLabel.grid(row=0, column=0)

    def get_time():
        timevar = time.strftime("%H:%M:%S:%p:%a \n %x")
        clock.config(text=timevar)
        clock.after(200, get_time)

    clock = Label(home_window, font=('Barlow Bold', 14), bg='#C0FFBC', fg='#0C4E1B')
    clock.place(x=1000, y=10)
    get_time()

    def Records():
        home_window.destroy()
        records()

    def TAKE_ATTENDANCE():
        home_window.destroy()
        attendance()

    def LOGOUT():
        messagebox.showinfo('Success!!', 'Logout Successful!')
        home_window.destroy()
        qr()

    profileEntry = Button(home_window, text='MANAGE STUDENTS', width=19, height=2, font=('Barlow Light', 14, 'bold'),
                          bg='#C0FFBC', fg='#0C4E1B'
                          , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0, command=Records)
    profileEntry.place(x=290, y=6)

    profileEntry = Button(home_window, text='ATTENDANCE', width=19, height=2, font=('Barlow Light', 14, 'bold'),
                          bg='#C0FFBC', fg='#0C4E1B'
                          , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0,
                          command=TAKE_ATTENDANCE)
    profileEntry.place(x=560, y=6)

    profileEntry = Button(home_window, text='LOGOUT', width=10, height=2, font=('Barlow Light', 14, 'bold'),
                          bg='#C0FFBC', fg='#0C4E1B'
                          , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0, command=LOGOUT)
    profileEntry.place(x=810, y=6)

    home_window.mainloop()


def records():
    root = Tk()
    root.title('STUDENT RECORDS')
    root.geometry('1156x650+120+30')
    root.iconbitmap('D:/dist - Copy/logo.ico')
    root.resizable(0, 0)
    bgImage = ImageTk.PhotoImage(file='D:/dist - Copy/students.png')
    bgLabel = Label(root, image=bgImage)
    bgLabel.place(y=0, anchor=NW)
    root.iconbitmap('D:/dist - Copy/logo.ico')

    def get_time():
        timevar = time.strftime("%H:%M:%S:%p:%a \n %x")
        clock.config(text=timevar)
        clock.after(200, get_time)

    clock = Label(root, font=('Barlow Bold', 14), bg='#C0FFBC', fg='#0C4E1B')
    clock.place(x=1000, y=10)
    get_time()

    def TAKE_ATTENDANCE():
        root.destroy()
        attendance()

    def home():
        root.destroy()
        homes()

    def LOGOUT():
        tkMessagebox.showinfo('Success!!', 'Logout Successful!')
        root.destroy()
        qr()



    parser = ConfigParser()
    parser.read("D:/dist - Copy/treebase.ini")
    saved_primary_color = parser.get('colors', 'primary_color')
    saved_highlight_color = parser.get('colors', 'highlight_color')

    def database():

        for record in my_tree.get_children():
            my_tree.delete(record)

        conn = sqlite3.connect('D:/dist - Copy/attendance0.db')
        c = conn.cursor()

        c.execute("select * from records")
        data = c.fetchall()

        global count
        count = 0
        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]),
                               tags=("evenrow"))
            else:
                my_tree.insert(parent="", index="end", text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]),
                               tags=("oddrow"))

        count += 1

        conn.commit()
        conn.close()

    def primary_color():
        primary_color = colorchooser.askcolor()[1]
        if primary_color:
            # my_tree.tag_configure('oddrow', background='white')
            my_tree.tag_configure('evenrow', background=primary_color)

            parser = ConfigParser()
            parser.read('treebase.ini')
            parser.set('colors', 'primary_color', primary_color)

            with open('treebase.ini', 'w') as configfile:
                parser.write(configfile)

    def highlight_color():
        highlight_color = colorchooser.askcolor()[1]
        if highlight_color:
            style.map('Treeview', background=[('selected', highlight_color)])

            parser = ConfigParser()
            parser.read('D:/dist - Copy/treebase.ini')
            parser.set('colors', 'highlight_color', highlight_color)

            with open('D:/dist - Copy/treebase.ini', 'w') as configfile:
                parser.write(configfile)

    def reset_colors():
        parser = ConfigParser()
        parser.read('D:/dist - Copy/treebase.ini')
        parser.set('colors', 'primary_color', 'lightgreen')
        parser.set('colors', 'highlight_color', 'darkgreen')
        with open('D:/dist - Copy/treebase.ini', 'w') as configfile:
            parser.write(configfile)
        my_tree.tag_configure('evenrow', background='lightgreen')
        style.map('Treeview', background=[('selected', 'darkgreen')])

    my_menu = Menu(root)
    root.config(menu=my_menu)

    option_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Options", menu=option_menu)

    option_menu.add_command(label="Primary Color", command=primary_color)
    option_menu.add_command(label="Highlight Color", command=highlight_color)
    option_menu.add_separator()
    option_menu.add_command(label="Exit", command=root.quit)

    option_menu.add_command(label="Reset Colors", command=reset_colors)
    option_menu.add_separator()

    def search_records():
        lookup_records = search_entry.get()

        search.destroy()

        for record in my_tree.get_children():
            my_tree.delete(record)

        conn = sqlite3.connect('D:/dist - Copy/attendance0.db')
        c = conn.cursor()

        c.execute("select * from records where name like ?", (lookup_records,))
        data = c.fetchall()

        global count
        count = 0
        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]),
                               tags=("evenrow"))
            else:
                my_tree.insert(parent="", index="end", text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]),
                               tags=("oddrow"))

        count += 1

        conn.commit()
        conn.close()

    def lookup_records():
        global search_entry, search
        search = Toplevel(root)
        search.title("Lookup Records")
        search.geometry("400x200")

        search_frame = LabelFrame(search, text="Search Name")
        search_frame.pack(padx=10, pady=10)

        search_entry = Entry(search_frame, font=("Barlow Light", 15))
        search_entry.pack(pady=20, padx=20)

        search_button = Button(search, text="Search Records", command=search_records)
        search_button.pack(padx=20, pady=20)

    def records():
        records()

    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Search", menu=search_menu)
    search_menu.add_command(label="Search", command=lookup_records)
    search_menu.add_separator()
    search_menu.add_command(label="Reset", command=database)

    style = ttk.Style()
    style.theme_use('default')

    style.configure("Treeview", background="#A0F18D", foreground="black", rowheight="25", fieldbackground="white")
    style.map('Treeview', background=[('selected', saved_highlight_color)])

    tree_frame = Frame(root)
    tree_frame.pack(pady=80)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='browse')

    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ('School ID', 'Name', 'Gender', 'Email', 'Grade', 'Sector', 'Birthday', 'Section')
    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('School ID', width=120, anchor=CENTER)
    my_tree.column('Name', width=120, anchor=CENTER)
    my_tree.column('Gender', width=120, anchor=CENTER)
    my_tree.column('Email', width=120, anchor=CENTER)
    my_tree.column('Grade', width=120, anchor=CENTER)
    my_tree.column('Sector', width=120, anchor=CENTER)
    my_tree.column('Birthday', width=120, anchor=CENTER)
    my_tree.column('Section', width=120, anchor=CENTER)

    my_tree.heading('#0', text="", anchor=W)
    my_tree.heading('School ID', text="School ID", anchor=CENTER)
    my_tree.heading('Name', text="Name", anchor=CENTER)
    my_tree.heading('Gender', text="GENDER", anchor=CENTER)
    my_tree.heading('Email', text="EMAIL", anchor=CENTER)
    my_tree.heading('Grade', text="GRADE", anchor=CENTER)
    my_tree.heading('Sector', text="SECTOR", anchor=CENTER)
    my_tree.heading('Birthday', text="BIRTHDAY", anchor=CENTER)
    my_tree.heading('Section', text="SECTION", anchor=CENTER)
    my_tree.tag_configure('oddrow', background='white')
    my_tree.tag_configure('evenrow', background=saved_primary_color)


    sf = Label(root, text='Student Form', font=('Barlow Medium', 13), foreground="#0C4E1B", bg='#C0FFBC').place(x=90,y=350)
    i1 = Label(root, text='School ID', font=('Barlow Medium', 14), foreground="#0C4E1B", bg='#A0F18D').place(x=90, y=400)
    nl = Label(root, text='Name', font=('Barlow Medium', 14), foreground="#0C4E1B", bg='#A0F18D').place(x=90,y=450)
    gl = Label(root, text='Gender', font=('Barlow Bold', 14), foreground="#0C4E1B", bg='#A0F18D').place(x=90, y=500)
    el = Label(root, text='Email', font=('Barlow Bold', 14), foreground="#0C4E1B", bg='#A0F18D').place(x=430, y=400)
    grl = Label(root, text='Grade', font=('Barlow Bold', 14), foreground="#0C4E1B", bg='#A0F18D').place(x=750,y=400)
    sl = Label(root, text='Sector', font=('Barlow Bold', 14), foreground="#0C4E1B", bg='#A0F18D').place(x=430,y=450)
    bl = Label(root, text='Birthday', font=('Barlow Bold', 14), foreground="#0C4E1B", bg='#A0F18D').place(x=430,y=500)
    secl = Label(root, text='Section', font=('Barlow Bold', 14), foreground="#0C4E1B", bg='#A0F18D').place(x=750,y=450)


    schoolid_box = Entry(root, width=20, font=('Barlow Light', 15), foreground="#0C4E1B")
    schoolid_box.place(x=200, y=400)
    name_box = Entry(root, width=20, font=('Barlow Light', 15), foreground="#0C4E1B")
    name_box.place(x=200, y=450)
    gender_box = ttk.Combobox(root, font=("Barlow Medium", 16), foreground="#0C4E1B")
    gender_box['state']='readonly'
    gender_box.set('Gender')
    gender_box["values"] = ("Male", "Female")
    gender_box.place(x=200,y=500, width=226)
    email_box = Entry(root, width=20, font=('Barlow Light', 15), foreground="#0C4E1B")
    email_box.place(x=515, y=400)
    grade_box = Entry(root, width=20, font=('Barlow Light', 15), foreground="#0C4E1B")
    grade_box.place(x=830, y=400)
    sector_box = ttk.Combobox(root, font=("Barlow Medium", 16), foreground="#0C4E1B")
    sector_box['state']='readonly'
    sector_box.set('Sector')
    sector_box["values"] = ("Student", "Teacher")
    sector_box.place(x=515, y=450, width=226)
    birthday_box = Entry(root, width=20, font=('Barlow Light', 15), foreground="#0C4E1B")
    birthday_box.place(x=515, y=500)
    section_box = Entry(root, width=20, font=('Barlow Light', 15), foreground="#0C4E1B")
    section_box.place(x=830, y=450)


    def add_record():
        name = name_box.get()
        SI = schoolid_box.get()
        genders = gender_box.get()
        emails = email_box.get()
        grades = grade_box.get()
        sectors = sector_box.get()
        births = birthday_box.get()
        sections = section_box.get()

        if name == '':
            messagebox.showerror('Error', 'Please Enter a Name! ')
        elif SI == '':
            messagebox.showerror('Error', 'Please Enter a SchoolID! ')
        elif genders == 'Gender' or '':
            messagebox.showerror('Error', 'Please Enter a Gender! ')
        elif sectors == 'Sector' or '':
            messagebox.showerror('Error', 'Please Enter a Sector! ')
        elif emails == '':
            messagebox.showerror('Error', 'Please Enter an Email! ')
        elif grades == '':
            messagebox.showerror('Error', 'Please Enter a Grade! ')
        elif births == '':
            messagebox.showerror('Error', 'Please Enter a valid date of birth! ')
        elif sections == '':
            messagebox.showerror('Error', 'Please Enter a Section! ')
        else:
            conn = sqlite3.connect('D:/dist - Copy/attendance0.db')
            c = conn.cursor()
            c.execute(
                "insert into records values (:idd, :name, :gender, :email, :grade, :sector, :birthday, :section)",
                {
                    'idd': schoolid_box.get(),
                    'name': name_box.get(),
                    'gender': gender_box.get(),
                    'email': email_box.get(),
                    'grade': grade_box.get(),
                    'sector': sector_box.get(),
                    'birthday': birthday_box.get(),
                    'section': section_box.get()
                })

            conn.commit()
            conn.close()

            schoolid_box.delete(0, END)
            name_box.delete(0, END)
            gender_box.delete(0, END)
            email_box.delete(0, END)
            grade_box.delete(0, END)
            sector_box.delete(0, END)
            birthday_box.delete(0, END)
            section_box.delete(0, END)

            my_tree.delete(*my_tree.get_children())
            database()
            tkMessagebox.showinfo("Added!", "Your information has been added!")

    add_record = Button(root, text='Add Record', font=("Barlow Medium", 14), width=15, cursor='hand2', fg='white',
                        bg='#0C4E1B', activebackground='#A0F18D', bd=0, command=add_record)
    add_record.place(x=890,y=550)

    def remove_all():
        for record in my_tree.get_children():
            my_tree.delete(record)

    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = sqlite3.connect('D:/dist - Copy/attendance0.db')
        c = conn.cursor()
        c.execute("delete from records where idd =" + schoolid_box.get())

        schoolid_box.delete(0, END)
        name_box.delete(0, END)
        gender_box.delete(0, END)
        email_box.delete(0, END)
        grade_box.delete(0, END)
        sector_box.delete(0, END)
        birthday_box.delete(0, END)
        section_box.delete(0, END)

        tkMessagebox.showerror("Deleted!", "Your record has been deleted!")
        conn.commit()
        conn.close()
        my_tree.delete(*my_tree.get_children())
        database()

    remove_one = Button(root, text="Remove", font=("Barlow Medium", 14), width=15, fg='white', bg='#0C4E1B',
                        activebackground='#A0F18D', cursor='hand2', bd=0, command=remove_one)
    remove_one.place(x=620,y=550)

    def select_record():
        schoolid_box.delete(0, END)
        name_box.delete(0, END)
        gender_box.delete(0, END)
        email_box.delete(0, END)
        grade_box.delete(0, END)
        sector_box.delete(0, END)
        birthday_box.delete(0, END)
        section_box.delete(0, END)

        selected = my_tree.focus()

        values = my_tree.item(selected, 'values')
        schoolid_box.insert(1, values[0])
        name_box.insert(2, values[1])
        gender_box.insert(3, values[2])
        email_box.insert(4, values[3])
        grade_box.insert(5, values[4])
        sector_box.insert(6, values[5])
        birthday_box.insert(7, values[6])
        section_box.insert(8, values[7])

    def update_record():
        selected = my_tree.focus()
        my_tree.item(selected, text="", values=(schoolid_box.get(), name_box.get(), gender_box.get(), email_box.get(), grade_box.get(),sector_box.get(), birthday_box.get(), section_box.get()))

        conn = sqlite3.connect('D:/dist - Copy/attendance0.db')
        c = conn.cursor()
        c.execute("""UPDATE records SET 


                  name = :names,
                  gender = :genders,
                  email = :emails,  
                  grade = :grades,
                  sector = :sectors,
                  birthday = :birthdays,
                  section = :sections

                  WHERE idd = :idd""",
                  {
                      'idd': schoolid_box.get(),
                      'names': name_box.get(),
                      'genders': gender_box.get(),
                      'emails': email_box.get(),
                      'grades': grade_box.get(),
                      'sectors': sector_box.get(),
                      'birthdays': birthday_box.get(),
                      'sections': section_box.get()

                  })

        tkMessagebox.showinfo("Updated!", "Your record has been updated!")
        conn.commit()
        conn.close()

        schoolid_box.delete(0, END)
        name_box.delete(0, END)
        gender_box.delete(0, END)
        email_box.delete(0, END)
        grade_box.delete(0, END)
        sector_box.delete(0, END)
        birthday_box.delete(0, END)
        section_box.delete(0, END)

    def clicker(e):
        select_record()

    select_button = Button(root, text='Select Record', font=("Barlow Medium", 14), fg='white', width=15,
                           bg='#0C4E1B', activebackground='#A0F18D', cursor='hand2', bd=0, command=select_record)
    select_button.place(x=90,y=550)

    update_button = Button(root, text='Update Record', font=("Barlow Medium", 14), fg='white', width=15,
                           bg='#0C4E1B', activebackground='#A0F18D', cursor='hand2', bd=0, command=update_record)
    update_button.place(x=350,y=550)

    my_tree.bind("<ButtonRelease-1>", clicker)

    recordsbutton = Button(root, text='ATTENDANCE', width=19, height=2, font=('Barlow Light', 14, 'bold'),
                           bg='#C0FFBC', fg='#0C4E1B'
                           , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0,
                           command=TAKE_ATTENDANCE)
    recordsbutton.place(x=560, y=8)

    homebutton = Button(root, text='HOMEPAGE', width=13, height=2, font=('Barlow Light', 14, 'bold'), bg='#C0FFBC',
                        fg='#0C4E1B'
                        , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0, command=home)
    homebutton.place(x=115, y=8)

    logoutbutton = Button(root, text='LOGOUT', width=10, height=2, font=('Barlow Light', 14, 'bold'), bg='#C0FFBC',
                          fg='#0C4E1B'
                          , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0,
                          command=LOGOUT)
    logoutbutton.place(x=810, y=8)

    database()
    root.mainloop()



def attendance():
    root = tk.Tk()
    root.geometry("1156x650+120+30")
    root.title("Student Management System")
    bgImage = ImageTk.PhotoImage(file='D:/dist - Copy/attendances.png')
    bgLabel = Label(root, image=bgImage)
    bgLabel.pack()
    root.resizable(0, 0)
    root.iconbitmap('D:/dist - Copy/logo.ico')

    my_frame = Frame(root)
    my_frame.place(x=430, y=130)
    tree_frame = Frame(my_frame)
    tree_frame.pack()

    my_treee = ttk.Treeview(tree_frame,height=16)

    def file_open():
        filename = filedialog.askopenfilename(
            initialdir="D:/dist - Copy",
            title="Open a file..",
            filetype=(("csv files", "*.csv"), ("All Files", "*.*")))
        if filename:
            try:
                filename = r"{}".format(filename)
                df = pd.read_csv(filename)
                clear_tree()

                my_treee["column"] = list(df.columns)
                my_treee["show"] = "headings"

                for column in my_treee["column"]:
                    my_treee.heading(column, text=column)

                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    my_treee.insert("", "end", values=row)

                my_treee.pack()

            except ValueError:
                label.config(text="File couldn't be opened")
            except FileNotFoundError:
                label.config(text="File couldn't be found")

    def clear_tree():
        my_treee.delete(*my_treee.get_children())

    my_menu = Menu(root)
    root.config(menu=my_menu)
    filemenu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="Spreadsheet", menu=filemenu)
    filemenu.add_command(label="Open", command=file_open)
    label = Label(root, text='')
    label.pack(pady=20)

    def get_time():
        timevar = time.strftime("%H:%M:%S:%p:%a \n %x")
        clock.config(text=timevar)
        clock.after(200, get_time)

    clock = Label(root, font=('Barlow Bold', 14), bg='#C0FFBC', fg='#0C4E1B')
    clock.place(x=1000, y=8)
    get_time()

    def Records():
        root.destroy()
        records()

    def home():
        root.destroy()
        homes()

    def LOGOUT():
        tkMessagebox.showinfo('Success!!', 'Logout Successful!')
        root.destroy()
        qr()

    profileEntry = Button(root, text='MANAGE STUDENTS', width=19, font=('Barlow Light', 14, 'bold'),
                          bg='#C0FFBC', fg='#0C4E1B'
                          , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0,
                          command=Records)
    profileEntry.place(x=290, y=8)

    homebutton = Button(root, text='HOMEPAGE', width=13, font=('Barlow Light', 14, 'bold'), bg='#C0FFBC',
                        fg='#0C4E1B'
                        , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0, command=home)
    homebutton.place(x=115, y=8)

    logoutbutton = Button(root, text='LOGOUT', width=10, font=('Barlow Light', 14, 'bold'), bg='#C0FFBC',
                          fg='#0C4E1B'
                          , activebackground='#0C4E1B', activeforeground='#C0FFBC', cursor='hand2', bd=0,
                          command=LOGOUT)
    logoutbutton.place(x=795, y=8)

    root.mainloop()


qr()
