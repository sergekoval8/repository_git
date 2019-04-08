from tkinter import *
import json
import re
from arduino_ports import serial_ports
from sms_sender import sms_send

SELECT_N=None
Port=None
phone=None

top= Tk()

def open_file():
    # of = askopenfilename()                       # -  на этапе первичного сздания  базы номеров ?
    of='base_telefon_.txt'
    base=[]
    try:
        with open(of,"r",encoding='utf-8') as file:
            base_txt=json.load(file)
        for el in base_txt:
            print(el)
            base.append({'descr':(el['descr']),'num':(el['num'])})
    except Exception:
        pass
    return base

def save_file():
    # sf = asksaveasfilename()    -  на этапе первичного сoздания  базы номеров ?
    sf = 'base_telefon_.txt'
    file = open(sf, "w",encoding="utf-8")
    json.dump(base,file,indent=4)
    file.close()

def exit_ap():
    top.quit()

def add_next(event):                                          # Добавление номеров
    num = num_field.get()
    patt="7"+"[0-9]{10}"
    descr=descript.get()
    if num == '':
        var_add.set("не указан телефон")
    elif not re.match(patt,num) or len(num)>11:
        var_add.set(' не корректный номер, номер должен начинаться с "7"(без знака "+") и состоять из 11 цифр')
    elif descr == '':
        var_add.set("не указана метка")
    elif any(el['descr']==descr  for el in  base):
        var_add.set("не уникальный дескиптор")
    else:
        base.append({'descr':descr,'num':num})
        save_file()
        var_add.set("номер добавлен")
        represent_base()


def represent_base():                                       # Вываливаем базу номеров
    tx.delete(1, END)
    for i in range(len(base)):
        tx.insert(i,f"{base[i]['descr']:<30}        {base[i]['num']:>11}")

def index_base_list(event):                                 #iter
    try:
        global SELECT_N , phone
        SELECT_N = tx.curselection()[0]
        phone=base[SELECT_N]['num']
        var_desc.set(base[SELECT_N]['descr'])
        var_num.set(phone)
    except IndexError:
        pass
    res_var.set("")


def station_reload(event):
    global SELECT_N, Port, phone
    if SELECT_N is not None and Port is not None:
        res_var.set("Сигнал отправлен")
        print(f'Phone is {phone}')
        sms_answ = sms_send(Port, phone)

        print(f'sms_answ {sms_answ}')
        SELECT_N = None                                                 #        сброс выбранных опций
        text_port.set("Не выбран")
        var_desc.set("")
        var_num.set("")
        confirm.set(2)
        res_var.set(sms_answ)

def confirmat():
    global SELECT_N
    if SELECT_N is not None:
        answ=confirm.get()
        if answ==1:
            selection = "выбран "
            res_var.set("")
        else:
            selection = "Не выбран "
            SELECT_N=None
        text_port.set(selection)

def port_seek(event):
    global ports
    ports=serial_ports()
    print(ports)
    place_ports()

def place_ports():
    num_port = len(ports)
    text_info = "Проверьте подключение контроллера" if num_port == 0 else f"Обнаружено {num_port} портов"
    text_inf.set(text_info)
    for i, port in enumerate(ports):
        print(port)
        c, v = port
        print(v)
        pi = Radiobutton(fra1, text=f"{v}", variable=var_port, value=i + 1, command=port_sel)
        pi.grid(row=4, column=i)
    pi = Radiobutton(fra1, text="не выбран", variable=var_port, value=num_port+1, command=port_sel)
    pi.grid(row=4, column=num_port)

def port_sel():
    global Port, ports
    print(var_port.get())
    # import ipdb; ipdb.set_trace()
    Port=ports[var_port.get()-1][0] if var_port.get()<=len(ports) else None
    print(Port)



base=open_file()

main_menu=Menu(top)
ports=serial_ports()
top.configure(menu=main_menu)


first_item=Menu(main_menu,tearoff=0)
main_menu.add_cascade(label="FILE",menu=first_item)

first_item.add_command(label="Show",command=represent_base)
first_item.add_command(label="Save_to_Json",command=save_file)   #  проверить : есть ли смысл ?
first_item.add_command(label="Exit",command=exit_ap)

sec_item=Menu(main_menu,tearoff=0)
main_menu.add_cascade(label="edit_base",menu=sec_item)
sec_item.add_command(label="edit_base",command=None)
sec_item.add_cascade(label="choose_port",command=None)           # через явное представление пока что


fra0=Frame(top,width=700,height=50,bg="gray")         #decorate
fra1 = Frame(top,width=700,height=300,bg="gray")       #  поле управления перезагрузкой
fra2 = Frame(top,width=700,height=500,bg="darkred")     #  поле управления списком       ---) удаление??- права??
fra3 = Frame(top,width=700,height=200,bg="gray",bd=20) #  поле добавления списка станций
#fra4 = Frame(top,width=500,height=150,bg="white")    # информационное: статистика по перезагрузкам

fra0.pack()
fra1.pack()
fra2.pack()
fra3.pack()
#fra4.pack()

 #-------------------------------------------fra1-------------------------------------------------                                                                                                                                                                       #
var_desc=StringVar()
var_num=StringVar()
text_port=StringVar()
lab_des = Label(fra1, text="Проверьте метку станции", font="Arial 10")
descr_reload=Label(fra1,textvariable=var_desc,width=20,borderwidth =3,relief = RAISED)
lab_num = Label(fra1, text="Проверьте номер станции", font="Arial 10")
num_reload=Label(fra1,textvariable=var_num,width=20,borderwidth =3,relief = RAISED)
confirm = IntVar()
R1 = Radiobutton(fra1, text = "Выбор сделан?", variable = confirm, value = 1, command = confirmat)
R2 = Radiobutton(fra1, text = "Нет", variable = confirm, value = 2, command = confirmat)
lab_port = Label(fra1,textvariable=text_port,width=30,borderwidth =3,relief = RAISED)


but_reload = Button(fra1,text="Перезагрузить станцию",width=20,height=3,bg="white",fg="blue")
res_var = StringVar()
res_mes = Label( fra1, textvariable = res_var, width=30,height=2, relief = RAISED )


text_inf=StringVar()
lab_inf=Label(fra1, textvariable = text_inf, width=30,height=2, relief = RAISED)
but_seek=Button(fra1,text="Проверить порт",width=20,height=2,bg="white",fg="blue")

var_port = IntVar()
place_ports()
lab_des.grid(row=0,column=0)
descr_reload.grid(row=0,column=1)
lab_num.grid(row=0,column=2)
num_reload.grid(row=0,column=3)

R1.grid(row=1,column=0 )
R2.grid(row=1,column=1 )
but_reload.grid(row=1,column=2)
but_reload.bind("<Button-1>",station_reload)
res_mes.grid(row=1,column=3)

lab_port.grid(row=2,columnspan=2)

lab_inf.grid(row=3,columnspan=3)
but_seek.grid(row=3,column=3)
but_seek.bind("<Button-1>",port_seek)


#----------------------------------------------------------------------fra2----------------------------------
tx = Listbox(fra2,width=60,selectmode=SINGLE,height=10,font='12')
scr = Scrollbar(fra2,command=tx.yview)
tx.configure(yscrollcommand=scr.set)
tx.bind("<Button-1>", index_base_list)
tx.grid(row=0,column=0)
scr.grid(row=0,column=1)


#------------------------------------------------------------------------fra3-----------------------------------
descript=Entry(fra3,width=20,borderwidth =3)
lab1 = Label(fra3, text="Добавьте метку станции", font="Arial 10")
num_field=Entry(fra3,width=20,borderwidth =3)
# lab2 = Label(fra3, text=" а также", font="Arial 8")
lab3 = Label(fra3, text="Внесите номер станции", font="Arial 10")

lab1.grid(row=0,column=0)
descript.grid(row=0,column=1)
# lab2.grid(row=0,column=2)
lab3.grid(row=0,column=3)
num_field.grid(row=0,column=4)

but = Button(fra3,text="Добавить номер",width=20,height=3,bg="white",fg="blue")
var_add = StringVar()
mes = Label( fra3, textvariable = var_add, width=30,height=3, relief = RAISED )

but.bind("<Button-1>",add_next)
mes.grid(row=1,columnspan=2)
but.grid(row=1,column=2)


top.mainloop()

#
