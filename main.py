from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from database import DataBase
from functions import HOG
import os

db = DataBase()

root = Tk()
root.title('Вход')
root.geometry('925x500+300+200')
root.configure(bg='#FFFFFF')
root.resizable(False, False)

img = PhotoImage(file=r'..\pythonProject\login.png')
Label(root, image=img, bg='#FFFFFF').place(x=50, y=50)

def mainfunc():
    def close():
        if messagebox.askokcancel("Выход из приложения", "Хотите закрыть приложение?"):
            screen.destroy()

    number = 20
    def makeResponse():
        text = req.get()
        image = path.get()
        number = int(clicked.get())
        multicolor = multicolor_var.get()
        if (text and image) and (text!='Описание' and image!="Изображение"):

            func = HOG()
            flag = db.check_pictures(text)
            if not flag:
                func.getImages(req.get(), db)
            picts_data = db.get_images(text)
            res = func.findSamiestPict(image, picts_data, multicolor)
            ids = list(res.values())
            p = rf"..\pythonProject\Результат\{text}"
            os.mkdir(p)
            for i in range(number):
                image = db.get_image_by_id(ids[i])
                func.Binary_To_File_Save(image[0], text, str(i+1))
            p = os.path.realpath(p)
            os.startfile(p)
            screen.destroy()
            mainfunc()
        else:
            messagebox.showerror('Ошибка!', 'Пустой запрос или не указан путь к файлу')

    def select_files():
        filetypes = [('image files', ('*.jpg', '*.png', '*.jpeg'))]
        filename = fd.askopenfilenames(title='Открыть изображение', initialdir='/', filetypes=filetypes)
        path.delete(0, 'end')
        path.insert(END, filename)


    screen = Tk()
    screen.protocol("WM_DELETE_WINDOW", close)
    screen.title("Поиск схожих картинок")
    screen.wm_attributes("-topmost", 1)
    screen.geometry("925x500+300+200")
    screen.configure(bg='#FFFFFF')
    screen.resizable(False, False)

    main_frame = Frame(screen, width=500, height=500, bg="#FFFFFF")
    main_frame.place(x=180, y=70)

    header = Label(main_frame, text='Поиск изображений', fg='#57a1f8', bg='#FFFFFF', font=("Arial", 23, 'bold'))
    header.place(x=100, y=5)

    # Запрос
    def on_enter(e):
        if req.get()=='Описание':
            req.delete(0, 'end')

    def on_leave(e):
        name = req.get()
        if name == '':
            req.insert(0, 'Описание')

    req = Entry(main_frame, width=25, fg='#333333', border=0, bg='#FFFFFF', font=("Arial", 13))
    req.place(x=30, y=80)
    req.insert(0, "Описание")
    req.bind('<FocusIn>', on_enter)
    req.bind('<FocusOut>', on_leave)

    Frame(main_frame, width=500, height=2, bg="#333333").place(x=25, y=107)

    # Путь
    def on_enter(e):
        if path.get()=='Изображение':
            path.delete(0, 'end')

    def on_leave(e):
        name = path.get()
        if name == '':
            path.insert(0, 'Изображение')

    path = Entry(main_frame, width=295, fg='#333333', border=0, bg='#FFFFFF', font=("Arial", 13))
    path.place(x=30, y=150)
    path.insert(0, "Изображение")
    path.bind('<FocusIn>', on_enter)
    path.bind('<FocusOut>', on_leave)

    Frame(main_frame, width=500, height=2, bg="#333333").place(x=25, y=177)

    Button(main_frame, width=19, pady=7, text='Выбрать изображение', bg='#57a1f8', fg='#FFFFFF', border=0, command=select_files).place(x=350,y=180)

    multicolor_var = BooleanVar()
    multicolor_var.set(False)
    Label(main_frame, text="Учитывать цвет:", bg='#FFFFFF', fg="#333333", font=("Arial", 13)).place(x=25, y=180)
    Checkbutton(main_frame, width=5, variable=multicolor_var, onvalue=True, offvalue=False , border=0, bg='white', fg='#57a1f8').place(x=200, y=185)


    Label(main_frame, text="Кол-во изображений\nдля скачивания:", bg='#FFFFFF', fg="#333333", font=("Arial", 13)).place(x=25, y=230)
    options = ['1','5','10','20','50','100']
    clicked = StringVar()
    clicked.set('20')
    drop = OptionMenu(main_frame, clicked, *options)
    drop.place(x=200, y=235)

    search_button = Button(main_frame, width=20, pady=10, text='Искать', font=("Arial", 16, 'bold'),bg='#57a1f8', fg='#FFFFFF', border=0, command=makeResponse)
    search_button.place(x=125,y=300)

    screen.mainloop()

def sigin():
    username = user.get()
    password = pwd.get()
    if db.check_user(username, password):
        messagebox.showinfo('Успех!','Вы успешно авторизовались!')
        root.destroy()
        mainfunc()
    else:
        messagebox.showerror('Ошибка!','Неверный логин или пароль!')

##########################РЕГИСТРАЦИЯ#################################
def tosigup():
    window = Toplevel(root)
    window.title('Регистрация')
    window.geometry('925x500+300+200')
    window.configure(bg='#FFFFFF')
    window.resizable(False, False)

    img = PhotoImage(file=r'..\pythonProject\reg.png')
    Label(window, image=img, bg='#FFFFFF').place(x=50, y=50)

    def sigup():
        username = user.get()
        password = pwd.get()
        copy_password = copy_pwd.get()
        if copy_password != password:
            messagebox.showerror('Ошибка!', 'Пароли не совпадают!')
        else:
            if not db.check_user(username, password):
                db.save_user(username, password)
                messagebox.showinfo('Успех!', 'Вы успешно зарегистрировались!')
                window.destroy()
            else:
                messagebox.showerror('Ошибка!', 'Данный логин уже занят!')

    def tosigin():
        window.destroy()

    frame = Frame(window, width=350, height=350, bg="#FFFFFF")
    frame.place(x=480, y=70)

    head = Label(frame, text='Регистрация', fg='#57a1f8', bg='#FFFFFF', font=("Arial", 23, 'bold'))
    head.place(x=100, y=5)

    # Логин
    def on_enter(e):
        if user.get()=='Логин':
            user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Логин')

    user = Entry(frame, width=25, fg='#333333', border=0, bg='#FFFFFF', font=("Arial", 11))
    user.place(x=30, y=80)
    user.insert(0, "Логин")
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg="#333333").place(x=25, y=107)

    # Пароль
    def on_enter(e):
        if pwd.get()=='Пароль':
            pwd.delete(0, 'end')

    def on_leave(e):
        name = pwd.get()
        if name == '':
            pwd.insert(0, 'Пароль')

    pwd = Entry(frame, width=25, fg='#333333', border=0, bg='#FFFFFF', font=("Arial", 11))
    pwd.place(x=30, y=150)
    pwd.insert(0, "Пароль")
    pwd.bind('<FocusIn>', on_enter)
    pwd.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg="#333333").place(x=25, y=177)

    # Повторение пароля
    def on_enter(e):
        if copy_pwd.get() == 'Повторите пароль':
            copy_pwd.delete(0, 'end')

    def on_leave(e):
        name = copy_pwd.get()
        if name == '':
            copy_pwd.insert(0, 'Повторите пароль')

    copy_pwd = Entry(frame, width=25, fg='#333333', border=0, bg='#FFFFFF', font=("Arial", 11))
    copy_pwd.place(x=30, y=220)
    copy_pwd.insert(0, "Повторите пароль")
    copy_pwd.bind('<FocusIn>', on_enter)
    copy_pwd.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg="#333333").place(x=25, y=247)

    Button(frame, width=39, pady=7, text='Зарегистрироваться', bg='#57a1f8', fg='#FFFFFF', border=0,
           command=sigup).place(x=35, y=280)
    label = Label(frame, text='Уже есть аккаунт?', fg='#333333', bg='#FFFFFF', font=("Arial", 9))
    label.place(x=90, y=320)

    sign_up = Button(frame, width=6, text='Войти', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=tosigin)
    sign_up.place(x=200, y=320)

    window.mainloop()

##########################################################


frame = Frame(root, width=350, height=350, bg="#FFFFFF")
frame.place(x=480,y=70)

head = Label(frame, text = 'Авторизация', fg = '#57a1f8', bg = '#FFFFFF', font=("Arial", 23, 'bold'))
head.place(x=100, y = 5)

#Логин
def on_enter(e):
    if user.get()=='Логин':
        user.delete(0, 'end')


def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0, 'Логин')


user = Entry(frame, width=25, fg='#333333', border=0, bg='#FFFFFF', font=("Arial", 11))
user.place(x=30, y=80)
user.insert(0, "Логин")
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg="#333333").place(x=25,y=107)


#Пароль
def on_enter(e):
    if pwd.get() == 'Пароль':
        pwd.delete(0, 'end')


def on_leave(e):
    name=pwd.get()
    if name=='':
        pwd.insert(0, 'Пароль')


pwd = Entry(frame, width=25, fg='#333333', border=0, bg='#FFFFFF', font=("Arial", 11))
pwd.place(x=30, y=150)
pwd.insert(0, "Пароль")
pwd.bind('<FocusIn>', on_enter)
pwd.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg="#333333").place(x=25,y=177)


Button(frame, width=39, pady=7, text='Войти', bg='#57a1f8', fg='#FFFFFF', border=0, command=sigin).place(x=35, y=204)
label=Label(frame, text='Нет аккаунта?', fg='#333333', bg='#FFFFFF', font=("Arial", 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=17, text='Зарегистрироваться', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=tosigup)
sign_up.place(x=215, y=270)


root.mainloop()