from sys import api_version
from tkinter import *
from tkinter import ttk
from unicodedata import category
from tkcalendar import Calendar, DateEntry
import csv, datetime
import re
import requests
import json


def centered(window, width, height):
    # Gets both half the screen width/height and window width/height
    positionRight = int(window.winfo_screenwidth()/2 - width/2)
    positionDown = int(window.winfo_screenheight()/2 - height/2)
    
    # Positions the window in the center of the page.
    window.geometry("+{}+{}".format(positionRight, positionDown))

# INPUT GROUP NAME SEE AGENDA CALENDARR
def inputGroupNameSAC(x):
    global ent_seeAgendaGroupNameCal
    if x == 2:
        namaGroupArr = []
        # Send get request to retrieve current user group
        get = requests.get(urlGetGroup, data={"username": username}, headers={"x-access-token": serverAccessToken})
        serverResp = json.loads(get.text)
        
        totalGroup = len(serverResp['group'])
        for i in range (totalGroup):
            namaGroupArr.insert(1,serverResp['group'][i]['nama_grup'])

        lbl_seeAgendaGroupNameCal = Label(frm_seeAgendaCal, text="Nama Grup", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        ent_seeAgendaGroupNameCal = ttk.Combobox(frm_seeAgendaCal,  width=10,values=namaGroupArr, font=("OpenSans", 10))
        ent_seeAgendaGroupNameCal.current(0)
        lbl_seeAgendaGroupNameCal.grid(column=1, row=4, padx=40, sticky="w")
        ent_seeAgendaGroupNameCal.grid(column=2, row=4, columnspan=2, sticky="w")
    else :
        lbl_seeAgendaGroupNameCal = Label(frm_seeAgendaCal, text=" ", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_seeAgendaGroupNameCal.grid(column=1, row=4, columnspan=4, sticky="we")

# INPUT GROUP NAME SEE AGENDA
def inputGroupNameSA(x, username, token):
    global ent_seeAgendaGroupName
    if x == 2:
        namaGroupArr = []
        # Send get request to retrieve current user group
        get = requests.get(urlGetGroup, data={"username": username}, headers={"x-access-token": token})
        serverResp = json.loads(get.text)
        totalGroup = len(serverResp['group'])
        for i in range (totalGroup):
            namaGroupArr.insert(1,serverResp['group'][i]['nama_grup'])

        lbl_seeAgendaGroupName = Label(frm_seeAgenda, text="Nama Grup", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        ent_seeAgendaGroupName = ttk.Combobox(frm_seeAgenda,  width=10, values=namaGroupArr, font=("OpenSans", 10))
        ent_seeAgendaGroupName.current(0)
        lbl_seeAgendaGroupName.grid(column=1, row=4, padx=40, sticky="w")
        ent_seeAgendaGroupName.grid(column=2, row=4, columnspan=2, sticky="w")
    else :
        lbl_seeAgendaGroupName = Label(frm_seeAgenda, text=" ", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_seeAgendaGroupName.grid(column=1, row=4, columnspan=4, sticky="we")

def SACdone():
    pop_viewAgendaCal.destroy()
    pop_seeAgendaCal.destroy()

def SAdone():
    pop_viewAgenda.destroy()
    pop_seeAgenda.destroy()

# submit see agenda 
def submitSA(username, token):
    global frm_viewAgenda
    global pop_viewAgenda
    
    pop_viewAgenda = Toplevel(homePg)
    pop_viewAgenda.title("ToDoList-view")
    pop_viewAgenda.rowconfigure(1, weight=1)
    pop_viewAgenda.columnconfigure(0, weight=1)
    pop_viewAgenda.minsize(500,230)
    centered (pop_viewAgenda, 500, 230)

    activityDate = ent_seeAgendaDate.get_date()
    activityDateFormatted = activityDate.strftime("%d/%m/%Y")
    
    # Get agenda by personal or group
    payload = {}
    categoryValue = categoryVar.get()
    if categoryValue == 1:
        payload['kategori'] = "PERSONAL"
    else:
        #prepare payload
        groupName = ent_seeAgendaGroupName.get()
        payload['kategori'] = "GRUP"
        payload['nama_grup'] = groupName
        
        # Send get request to retrieve group member by group name
        dataAngggota = requests.get(urlGetGroupMember, data= {"nama_grup":groupName }, headers={"x-access-token": token}).json()
        listAnggota = ""
        for anggota in dataAngggota['member']:
            if anggota == dataAngggota['member'][-1]:
                listAnggota += anggota['username']
            else:
                listAnggota += anggota['username'] + ', '

    payload['username'] = username
    payload['tanggal'] = activityDate.strftime("%Y-%m-%d")
    
    # Send get request to retrieve activity by payload
    data = requests.get(urlViewActivity, data=payload, headers={"x-access-token": token}).json()

    listKegiatan = []
    if "kegiatan" in data:
        for kegiatan in data['kegiatan']:
            listKegiatan.insert(1, kegiatan['kegiatan'])

    # view agenda Form - Header
    lbl_viewAgendaHeader = Label(pop_viewAgenda, text="Agenda " + activityDateFormatted, bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

    lbl_viewAgendaHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")
    
    # view agenda form body
    global frm_viewAgenda 
    frm_viewAgenda = Frame(pop_viewAgenda, bg="#FFFFFF")
    lbl_viewAgendaSpaceN = Label(frm_viewAgenda, bg="#FFFFFF")
    lbl_viewAgendaSpaceS = Label(frm_viewAgenda, bg="#FFFFFF")
    lbl_viewAgendaSpaceW = Label(frm_viewAgenda, bg="#FFFFFF")
    lbl_viewAgendaSpaceE = Label(frm_viewAgenda, bg="#FFFFFF")
    lbl_viewAgendaKategori = Label(frm_viewAgenda, text="Kategori:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    categoryValue = categoryVar.get()
    if categoryValue == 1:
        lbl_viewAgendaKategori1 = Label(frm_viewAgenda, text="Personal", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    else:
        lbl_viewAgendaKategori1 = Label(frm_viewAgenda, text="Grup", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    
    lbl_viewAgendaKegiatan = Label(frm_viewAgenda, text="Kegiatan:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")

    if categoryValue == 2:
        lbl_viewAgendaNamaGrup = Label(frm_viewAgenda, text="Nama Grup:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_viewAgendaNamaGrupData = Label(frm_viewAgenda, text=groupName, bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_viewAgendaNamaGrup.grid(column=1, row=2, padx=40, sticky="w")
        lbl_viewAgendaNamaGrupData.grid(column=2, row=2, padx=40, sticky="w")

        lbl_viewAgendaAnggota = Label(frm_viewAgenda, text="Anggota:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_viewAgendaAnggotaList = Label(frm_viewAgenda, text=listAnggota, bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_viewAgendaAnggota.grid(column=1, row=3, padx=40, sticky="w")
        lbl_viewAgendaAnggotaList.grid(column=2, row=3, padx=40, sticky="w")

    lbl_listAgendaKegiatan = Text(frm_viewAgenda, bg="#FFFFFF", font=("OpenSans",10), borderwidth=0, height=5 , yscrollcommand =True)

    if listKegiatan:
        for index,kegiatan in enumerate(listKegiatan):
            lbl_listAgendaKegiatan.insert(END, str(index+1) + ". " +kegiatan + '\n')
    else:
        lbl_listAgendaKegiatan.insert(END, "Tidak ada kegiatan.")
    lbl_listAgendaKegiatan.configure(state="disabled")
    
    btn_viewAgendaDone = Button(frm_viewAgenda, bg="#FFFFFF", image=photo_btnDone, cursor="hand2",  borderwidth=0, command=SAdone)
    lbl_viewAgendaSpaceN.grid(column=0, row=0, columnspan=4)
    lbl_viewAgendaSpaceS.grid(column=0, row=6, columnspan=4)
    lbl_viewAgendaSpaceW.grid(column=0, row=1, rowspan=5)
    lbl_viewAgendaSpaceE.grid(column=3, row=1, rowspan=5)
    lbl_viewAgendaKategori.grid(column=1, row=1, padx=40, sticky="w")
    lbl_viewAgendaKategori1.grid(column=2, row=1, padx=40, sticky="w")

    lbl_viewAgendaKegiatan.grid(column=1, row=4, sticky="n")
    lbl_listAgendaKegiatan.grid(column=2, row=4, padx=40, sticky="w")
    btn_viewAgendaDone.grid(column=1, row=6, columnspan=2, pady=5) 
    frm_viewAgenda.grid(column=0, row=1, sticky="ensw")
    frm_viewAgenda.rowconfigure([0,6], weight=1)
    frm_viewAgenda.columnconfigure([0,3], weight=1)

def seeAgenda(username, token):
    global frm_seeAgenda
    global pop_seeAgenda
    global ent_seeAgendaDate

    pop_seeAgenda = Toplevel(homePg)
    pop_seeAgenda.title("ToDoList-View Agenda")
    pop_seeAgenda.rowconfigure(1, weight=1)
    pop_seeAgenda.columnconfigure(0, weight=1)
    pop_seeAgenda.minsize(500,230)
    centered (pop_seeAgenda, 500, 230)

    global categoryVar
    categoryVar=IntVar()
    categoryVar.set(1)
    # see agenda Form - Header
    lbl_seeAgendaHeader = Label(pop_seeAgenda, text="Melihat Agenda", bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

    lbl_seeAgendaHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")

    # see agenda form body
    global frm_seeAgenda   
    global actDate
    actDate = StringVar()
    frm_seeAgenda = Frame(pop_seeAgenda, bg="#FFFFFF")
    lbl_seeAgendaSpaceN = Label(frm_seeAgenda, bg="#FFFFFF")
    lbl_seeAgendaSpaceS = Label(frm_seeAgenda, bg="#FFFFFF")
    lbl_seeAgendaSpaceW = Label(frm_seeAgenda, bg="#FFFFFF")
    lbl_seeAgendaSpaceE = Label(frm_seeAgenda, bg="#FFFFFF")
    lbl_seeAgendaDate = Label(frm_seeAgenda, text="Tanggal", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_seeAgendaDate = DateEntry(frm_seeAgenda, width=38, date_pattern="dd/mm/yy", bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000", textvariable = actDate)
    lbl_seeAgendaDateNote = Label(frm_seeAgenda, text="*) DD/MM/YY", bg="#FFFFFF", font=("OpenSans",8), anchor="w")
    lbl_seeAgendaCategory = Label(frm_seeAgenda, text="Kategori", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    btn_seeAgendaPersonal = Radiobutton(frm_seeAgenda, bg="#FFFFFF", activebackground="#000000", activeforeground="#FFFFFF",text="Personal", cursor="hand2",  borderwidth=1, variable=categoryVar, value=1, command=lambda :inputGroupNameSA(1, username, token))
    btn_seeAgendaGrup = Radiobutton(frm_seeAgenda, bg="#FFFFFF", activebackground="#000000", activeforeground="#FFFFFF", text="Grup", cursor="hand2",  borderwidth=1, variable=categoryVar, value=2, command=lambda: inputGroupNameSA(2, username, token))
    btn_seeAgendaSubmit = Button(frm_seeAgenda, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=lambda: submitSA(username, token))
    lbl_seeAgendaSpaceN.grid(column=0, row=0, columnspan=5)
    lbl_seeAgendaSpaceS.grid(column=0, row=7, columnspan=5)
    lbl_seeAgendaSpaceW.grid(column=0, row=1, rowspan=7)
    lbl_seeAgendaSpaceE.grid(column=3, row=1, rowspan=7, padx=20)
    lbl_seeAgendaDate.grid(column=1, row=1, padx=40, sticky="w")
    ent_seeAgendaDate.grid(column=2, row=1, columnspan=2, sticky="w")
    lbl_seeAgendaDateNote.grid(column=2, row=2, columnspan=2, sticky="w")
    lbl_seeAgendaCategory.grid(column=1, row=3, padx=40, sticky="w")
    btn_seeAgendaPersonal.grid(column=2, row=3, pady=10, sticky="w")
    btn_seeAgendaGrup.grid(column=3, row=3, pady=10, sticky="w")
    btn_seeAgendaSubmit.grid(column=1, row=6, columnspan=3, pady=5) 
    frm_seeAgenda.grid(column=0, row=1, sticky="ensw")
    frm_seeAgenda.rowconfigure([0,6], weight=1)
    frm_seeAgenda.columnconfigure([0,4], weight=1) 

# INPUT GROUP NAME DEL AGENDA
def inputGroupNameDA(x, username, token):
    global ent_delAgendaGroupName


    if x == 2:
        namaGroupArr = []

        # Send get request to retrieve current user group
        get = requests.get(urlGetGroup, data={"username": username}, headers={"x-access-token": token})
        serverResp = json.loads(get.text)
        totalGroup = len(serverResp['group'])
        for i in range (totalGroup):
            namaGroupArr.insert(1,serverResp['group'][i]['nama_grup'])

        lbl_delAgendaGroupName = Label(frm_delAgenda, text="Nama Grup", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        ent_delAgendaGroupName = ttk.Combobox(frm_delAgenda,  width=10, values=namaGroupArr, font=("OpenSans", 10))
        ent_delAgendaGroupName.current(0)
        lbl_delAgendaGroupName.grid(column=1, row=4, padx=40, sticky="w")
        ent_delAgendaGroupName.grid(column=2, row=4, columnspan=2, sticky="w")
    else :
        lbl_delAgendaGroupName = Label(frm_delAgenda, text=" ", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_delAgendaGroupName.grid(column=1, row=4, columnspan=4, sticky="we")

#Delete selected activity
def DAdone(username, token, date, activity):
    payload = {
        "username": username,
        "tanggal": date,
        "kegiatan": activity,
    }

    #Send post request to the server and remove selected activity
    resp = requests.post(urlDeleteActivity, data=payload, headers={"x-access-token": token}).json()

    if "message" in resp:
        print(resp['message'])

    pop_chooseDelAgenda.destroy()
    pop_delAgenda.destroy()

# submit del agenda
def submitDA(username,token):
    global frm_chooseDelAgenda
    global pop_chooseDelAgenda

    global AGNum
    AGNum = StringVar(pop_delAgenda)
    AGNum.set(0)
    
    pop_chooseDelAgenda = Toplevel(homePg)
    pop_chooseDelAgenda.title("ToDoList-delete")
    pop_chooseDelAgenda.rowconfigure(1, weight=1)
    pop_chooseDelAgenda.columnconfigure(0, weight=1)
    pop_chooseDelAgenda.minsize(500,230)
    centered (pop_chooseDelAgenda, 500, 230)

    activityDate = ent_delAgendaDate.get_date()
    
    activityDateFormatted = activityDate.strftime("%d/%m/%Y")

    # del agenda Form - Header
    lbl_chooseDelAgendaHeader = Label(pop_chooseDelAgenda, text="Agenda " + activityDateFormatted, bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

    lbl_chooseDelAgendaHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")
    
    # view agenda form body
    global frm_chooseDelAgenda 
    frm_chooseDelAgenda = Frame(pop_chooseDelAgenda, bg="#FFFFFF")
    lbl_chooseDelAgendaSpaceN = Label(frm_chooseDelAgenda, bg="#FFFFFF")
    lbl_chooseDelAgendaSpaceS = Label(frm_chooseDelAgenda, bg="#FFFFFF")
    lbl_chooseDelAgendaSpaceW = Label(frm_chooseDelAgenda, bg="#FFFFFF")
    lbl_chooseDelAgendaSpaceE = Label(frm_chooseDelAgenda, bg="#FFFFFF")
    lbl_chooseDelAgendaKategori = Label(frm_chooseDelAgenda, text="Kategori:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    categoryValue = categoryVar.get()
    if categoryValue == 1:
        lbl_chooseDelAgendaKategori1 = Label(frm_chooseDelAgenda, text="Personal", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    else:
        lbl_chooseDelAgendaKategori1 = Label(frm_chooseDelAgenda, text="Grup", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    lbl_chooseDelAgendaKegiatan = Label(frm_chooseDelAgenda, text="Agenda yang ingin dihapus:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")

    # Get agenda by personal or group
    payload = {}
    if categoryValue == 1:
        payload['kategori'] = "PERSONAL"
    else:
        payload['kategori'] = "GRUP"
        payload['nama_grup'] = ent_delAgendaGroupName.get()

    formattedDate = activityDate.strftime("%Y-%m-%d")

    payload['username'] = username
    payload['tanggal'] = formattedDate
    
    # Send get request to retrieve activity by payload
    data = requests.get(urlViewActivity, data=payload, headers={"x-access-token": token}).json()

    listValue = []
    if "kegiatan" in data:
        for kegiatan in data['kegiatan']:
            listValue.insert(1, kegiatan['kegiatan'])


    btn_chooseDelAgendaSubmit = Button(frm_chooseDelAgenda, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=lambda: DAdone(username, token, formattedDate, ent_chooseDelAgendaKegiatan.get()))
    
    if "kegiatan" in data:
        ent_chooseDelAgendaKegiatan = ttk.Combobox(frm_chooseDelAgenda, width=10, values=listValue, font=("OpenSans", 10))
        ent_chooseDelAgendaKegiatan.current(0)
        btn_chooseDelAgendaSubmit.grid(column=1, row=5, columnspan=2, pady=5) 
    else: 
        ent_chooseDelAgendaKegiatan = Label(frm_chooseDelAgenda, text="Tidak ada aktivitas yang ditemukan.", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    lbl_chooseDelAgendaSpaceN.grid(column=0, row=0, columnspan=4)
    lbl_chooseDelAgendaSpaceS.grid(column=0, row=6, columnspan=4)
    lbl_chooseDelAgendaSpaceW.grid(column=0, row=1, rowspan=5)
    lbl_chooseDelAgendaSpaceE.grid(column=3, row=1, rowspan=5)
    lbl_chooseDelAgendaKategori.grid(column=1, row=1, padx=40, sticky="w")
    lbl_chooseDelAgendaKategori1.grid(column=2, row=1, padx=40, sticky="w")
    lbl_chooseDelAgendaKegiatan.grid(column=1, row=3, padx=40, sticky="w")
    ent_chooseDelAgendaKegiatan.grid(column=2, row=3, padx=40, sticky="w")
    
    frm_chooseDelAgenda.grid(column=0, row=1, sticky="ensw")
    frm_chooseDelAgenda.rowconfigure([0,6], weight=1)
    frm_chooseDelAgenda.columnconfigure([0,3], weight=1)  

def delAgenda(username,token):
    global frm_delAgenda
    global pop_delAgenda
    global ent_delAgendaDate

    pop_delAgenda = Toplevel(homePg)
    pop_delAgenda.title("ToDoList-Delete Agenda")
    pop_delAgenda.rowconfigure(1, weight=1)
    pop_delAgenda.columnconfigure(0, weight=1)
    pop_delAgenda.minsize(500,230)
    centered (pop_delAgenda, 500, 230)

    global categoryVar
    categoryVar=IntVar()
    categoryVar.set(1) #set default value for category

    # del agenda Form - Header
    lbl_delAgendaHeader = Label(pop_delAgenda, text="Menghapus Agenda", bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

    lbl_delAgendaHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")

    # del agenda form body
    global frm_delAgenda 
    global actDate
    actDate = StringVar()
    frm_delAgenda = Frame(pop_delAgenda, bg="#FFFFFF")
    lbl_delAgendaSpaceN = Label(frm_delAgenda, bg="#FFFFFF")
    lbl_delAgendaSpaceS = Label(frm_delAgenda, bg="#FFFFFF")
    lbl_delAgendaSpaceW = Label(frm_delAgenda, bg="#FFFFFF")
    lbl_delAgendaSpaceE = Label(frm_delAgenda, bg="#FFFFFF")
    lbl_delAgendaDate = Label(frm_delAgenda, text="Tanggal", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_delAgendaDate = DateEntry(frm_delAgenda, width=38, date_pattern="dd/mm/yy", bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000", textvariable = actDate)
    lbl_delAgendaDateNote = Label(frm_delAgenda, text="*) DD/MM/YY", bg="#FFFFFF", font=("OpenSans",8), anchor="w")
    lbl_delAgendaCategory = Label(frm_delAgenda, text="Kategori", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    btn_delAgendaPersonal = Radiobutton(frm_delAgenda, bg="#FFFFFF", activebackground="#000000", activeforeground="#FFFFFF",text="Personal", cursor="hand2",  borderwidth=1, variable=categoryVar, value=1, command=lambda :inputGroupNameDA(1, username, token))
    btn_delAgendaGrup = Radiobutton(frm_delAgenda, bg="#FFFFFF", activebackground="#000000", activeforeground="#FFFFFF", text="Grup", cursor="hand2",  borderwidth=1, variable=categoryVar, value=2, command=lambda: inputGroupNameDA(2, username, token))
    btn_delAgendaSubmit = Button(frm_delAgenda, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=lambda: submitDA(username,token))
    
    lbl_delAgendaSpaceN.grid(column=0, row=0, columnspan=5)
    lbl_delAgendaSpaceS.grid(column=0, row=7, columnspan=5)
    lbl_delAgendaSpaceW.grid(column=0, row=1, rowspan=7)
    lbl_delAgendaSpaceE.grid(column=3, row=1, rowspan=7, padx=20)
    lbl_delAgendaDate.grid(column=1, row=1, padx=40, sticky="w")
    ent_delAgendaDate.grid(column=2, row=1, columnspan=2, sticky="w")
    lbl_delAgendaDateNote.grid(column=2, row=2, columnspan=2, sticky="w")
    lbl_delAgendaCategory.grid(column=1, row=3, padx=40, sticky="w")
    btn_delAgendaPersonal.grid(column=2, row=3, pady=10, sticky="w")
    btn_delAgendaGrup.grid(column=3, row=3, pady=10, sticky="w")
    btn_delAgendaSubmit.grid(column=1, row=6, columnspan=3, pady=5) 
    frm_delAgenda.grid(column=0, row=1, sticky="ensw")
    frm_delAgenda.rowconfigure([0,6], weight=1)
    frm_delAgenda.columnconfigure([0,4], weight=1) 

# INPUT GROUP NAME
def inputGroupName(x, username, token):
    global ent_addAgendaGroupName
    global test

    if x == 2:
        namaGroupArr = []
        # Send get request to retrieve current user group
        get = requests.get(urlGetGroup, data={"username": username}, headers={"x-access-token": token})
        print(get)
        print(get.text)
        serverResp = json.loads(get.text)
        # # print(serverResp['group'][0]['nama_grup']
        token = len(serverResp['group'])
        print(token)
        for i in range (token):
            namaGroupArr.insert (1,serverResp['group'][i]['nama_grup'])
            print(namaGroupArr[i])
        test =StringVar()
        test.set(namaGroupArr[0])
        lbl_addAgendaGroupName = Label(frm_addAgenda, text="Nama Grup", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        ent_addAgendaGroupName = ttk.Combobox(frm_addAgenda, width=10, textvariable=test, values=namaGroupArr, font=("OpenSans", 10))  
        lbl_addAgendaGroupName.grid(column=1, row=6, padx=40, sticky="w")
        ent_addAgendaGroupName.grid(column=2, row=6, columnspan=2, sticky="w")
    else :
        lbl_addAgendaGroupName = Label(frm_addAgenda, text=" ", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_addAgendaGroupName.grid(column=1, row=6, columnspan=4, sticky="we")
        


# SUBMIT ADD ACTIVITY
def submitact():
    global activityListNew

    activityList = ""

    for entries in activities:
        if str(entries.get())=="":
            addAgendaActivityInvalid = Label(frm_submit, text="Invalid! Masukkan seluruh kegiatan!\natau ubah jumlah kegiatan", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="center")
            addAgendaActivityInvalid.grid(column=0, row=0, columnspan=3, sticky="news")
            invalid = 1
            break
        else:
            activityList = activityList + str(entries.get()) + ","

            activityListNew = activityList.rstrip(",")  
            invalid = 0

    if invalid == 1:
        pop_addActivity.mainloop()
    else:    
        pop_addActivity.destroy()


# submit add agenda 
def submitAA(username, token):
    Num=AANum.get()

    valid=0

    if Num == "0":
        lbl_addAgendaNumInvalid = Label(frm_addAgenda, text="Invalid! Masukkan jumlah kegiatan!", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_addAgendaNumInvalid.grid(column=2, row=4, padx=40, sticky="ew")
        print("Jumlah Kegiatan Invalid!")
    else:
        lbl_addAgendaNumInvalid = Label(frm_addAgenda, text="Ok", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_addAgendaNumInvalid.grid(column=2, row=4, padx=40, sticky="ew")  
        print("Jumlah Kegiatan Valid!")
        valid = valid + 1  

    activityDate = ent_addAgendaDate.get_date()
    
    activityDateFormatted = activityDate.strftime("%Y-%m-%d")

    categoryValue = categoryVar.get()
    if categoryValue == 1:
        categoryValuePayload = "PERSONAL"
        valid = valid + 1
    else:
        categoryValuePayload = "GRUP"
        groupName = ent_addAgendaGroupName.get()
        # validating group name
        regexGN = "[^-\s]"
        # compiling regex
        patGN = re.compile(regexGN)
        # searching regex                 
        matGN = re.search(patGN, groupName)

        if matGN: 
            print("Valid Group Name")
            valid = valid + 1
            lbl_addAgendaGroupNameInvalid = Label(frm_addAgenda, text="Ok", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
            lbl_addAgendaGroupNameInvalid.grid(column=2, row=7, padx=40, sticky="we")
        else:
            print("Group Name Invalid!!") 
            lbl_addAgendaGroupNameInvalid = Label(frm_addAgenda, text="Invalid! Nama grup harus tanpa spasi", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
            lbl_addAgendaGroupNameInvalid.grid(column=2, row=7, padx=40, sticky="we")
    # print(test.get())
    if valid == 2:
        if categoryValue == 2:
            post = requests.post(urlAddActivity,data={"username": username, "tanggal": activityDateFormatted, "kegiatan": activityListNew, "kategori": categoryValuePayload, "nama_grup": test.get()}, headers={"x-access-token": token})
            print(post)
            print(post.text)
            pop_addAgenda.destroy()  
        else : 
            post = requests.post(urlAddActivity,data={"username": username, "tanggal": activityDateFormatted, "kegiatan": activityListNew, "kategori": categoryValuePayload}, headers={"x-access-token": token})
            print(post)
            print(post.text)
            pop_addAgenda.destroy()                  
    else:
        pop_addAgenda.mainloop() 


# FORM ADD ACTIVITY
def addActivity(username, token, event=None):
    Num = AANum.get()    


    global pop_addActivity
    global activities
    global frm_addActivity
    global frm_submit


    if Num == 0:
        lbl_addAgendaNumInvalid = Label(frm_addActivity, text="Mohon pilih jumlah kegiatan", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")  
        lbl_addAgendaNumInvalid.grid(column=2, row=4, padx=40, sticky="we")
        addAgenda(username, token)
    else:
        activities = []

        pop_addActivity = Toplevel(homePg)
        pop_addActivity.title("ToDoList-Add Activity")
        pop_addActivity.rowconfigure(1, weight=1)
        pop_addActivity.columnconfigure(0, weight=1)
        pop_addActivity.minsize(500,230)
        pop_addActivity.maxsize(500,230)
        centered (pop_addActivity, 500, 230)


        # add activity Form - Header
        lbl_headerddActivity = Label(pop_addActivity, text="Menambah Aktivitas", bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

        lbl_headerddActivity.grid(column=0, row=0, sticky="ensw")

        frm_canvas = Frame(pop_addActivity)
        frm_canvas.grid(column=0, row=1, sticky="news")
        frm_canvas.rowconfigure(0, weight=1)
        frm_canvas.columnconfigure(0, weight=1)        
        frm_submit = Frame(pop_addActivity, bg="#FFFFFF")
        frm_submit.grid(column=0, row=2, sticky="news")
        frm_submit.rowconfigure(0, weight=1)
        frm_submit.columnconfigure(0, weight=1)        
        
    
        frm_canvas.grid_propagate(False)

        canvas = Canvas(frm_canvas)
        canvas.grid(column=0, row=0, sticky="news")

        scrollbar=Scrollbar(frm_canvas, orient="vertical", command=canvas.yview)
        scrollbar.grid(column=1, row=0, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)    

        # add activity form body
        frm_addActivity = Frame(canvas, bg="#FFFFFF")    
        canvas.create_window((0,0), window=frm_addActivity, anchor="nw")
        lbl_addActivitySpaceN = Label(frm_addActivity, bg="#FFFFFF")
        lbl_addActivitySpaceS = Label(frm_addActivity, bg="#FFFFFF")
        lbl_addActivitySpaceW = Label(frm_addActivity, bg="#FFFFFF")
        lbl_addActivitySpaceE = Label(frm_addActivity, bg="#FFFFFF")
        


        for i in range(int(Num)): 
            lbl_addAgendaActivity = Label(frm_addActivity, text=f"Kegiatan ke-{i+1}", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
            ent_addAgendaActivity = Entry(frm_addActivity, text="", width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000")
            lbl_addAgendaActivity.grid(column=1, row=1+(i+1), padx=40, sticky="w",pady=5)
            ent_addAgendaActivity.grid(column=2, row=1+(i+1),  columnspan=2,  padx=40, pady=10, sticky="w")
            activities.append(ent_addAgendaActivity)

    
        lbl_addActivitySpaceN.grid(column=0, row=0, columnspan=4)
        lbl_addActivitySpaceS.grid(column=0, row=int(Num)+3, columnspan=4)
        lbl_addActivitySpaceW.grid(column=0, row=1, rowspan=int(Num)+3)
        lbl_addActivitySpaceE.grid(column=4, row=1, rowspan=int(Num)+3)
        frm_addActivity.update_idletasks()        

        btn_addAgendaSubmit = Button(frm_submit, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=submitact)
        btn_addAgendaSubmit.grid(column=0, row=1, columnspan=3, sticky="news", pady=5) 
        canvas.config(scrollregion=canvas.bbox("all"))    


        frm_canvas.config(width=500 + scrollbar.winfo_width(),height=230)     
        frm_addActivity.rowconfigure([0,(int(Num)+2)], weight=1)
        frm_addActivity.columnconfigure([0,5], weight=1)  
 

# FORM ADD AGENDA
def addAgenda(username, token):
    global frm_addAgenda
    global pop_addAgenda
    global ent_addAgendaDate

    pop_addAgenda = Toplevel(homePg)
    pop_addAgenda.title("ToDoList-Add Agenda")
    pop_addAgenda.rowconfigure(1, weight=1)
    pop_addAgenda.columnconfigure(0, weight=1)
    pop_addAgenda.minsize(500,230)
    centered (pop_addAgenda, 500, 230)

    global AANum
    AANum = StringVar(pop_addAgenda)
    AANum.set(0)

    global categoryVar
    categoryVar=IntVar()
    categoryVar.set(1)

    # add agenda Form - Header
    lbl_addAgendaHeader = Label(pop_addAgenda, text="Menambah Agenda", bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

    lbl_addAgendaHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")

    # add agenda form body
    global frm_addAgenda   
    global actDate
    actDate = StringVar()
    frm_addAgenda = Frame(pop_addAgenda, bg="#FFFFFF")
    lbl_addAgendaSpaceN = Label(frm_addAgenda, bg="#FFFFFF")
    lbl_addAgendaSpaceS = Label(frm_addAgenda, bg="#FFFFFF")
    lbl_addAgendaSpaceW = Label(frm_addAgenda, bg="#FFFFFF")
    lbl_addAgendaSpaceE = Label(frm_addAgenda, bg="#FFFFFF")
    lbl_addAgendaDate = Label(frm_addAgenda, text="Tanggal", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_addAgendaDate = DateEntry(frm_addAgenda, width=38, date_pattern="dd/mm/yy", bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000", textvariable = actDate)
    lbl_addAgendaDateNote = Label(frm_addAgenda, text="*) DD/MM/YY", bg="#FFFFFF", font=("OpenSans",8), anchor="w")
    lbl_addAgendaNum = Label(frm_addAgenda, text="Jumlah Kegiatan", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_addAgendaNum = ttk.Combobox(frm_addAgenda,  width=10, textvariable=AANum, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100], font=("OpenSans", 10))
    ent_addAgendaNum.bind("<<ComboboxSelected>>", lambda event:addActivity(username, token))  
    lbl_addAgendaCategory = Label(frm_addAgenda, text="Kategori", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    btn_addAgendaPersonal = Radiobutton(frm_addAgenda, bg="#FFFFFF", activebackground="#000000", activeforeground="#FFFFFF",text="Personal", cursor="hand2",  borderwidth=1, variable=categoryVar, value=1, command=lambda :inputGroupName(1, username, token))
    btn_addAgendaGrup = Radiobutton(frm_addAgenda, bg="#FFFFFF", activebackground="#000000", activeforeground="#FFFFFF", text="Grup", cursor="hand2",  borderwidth=1, variable=categoryVar, value=2, command=lambda: inputGroupName(2, username, token))
    btn_addAgendaSubmit = Button(frm_addAgenda, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=lambda: submitAA(username, token))
    
    lbl_addAgendaSpaceN.grid(column=0, row=0, columnspan=5)
    lbl_addAgendaSpaceS.grid(column=0, row=9, columnspan=5)
    lbl_addAgendaSpaceW.grid(column=0, row=1, rowspan=8)
    lbl_addAgendaSpaceE.grid(column=3, row=1, rowspan=8, padx=20)
    lbl_addAgendaDate.grid(column=1, row=1, padx=40, sticky="w")
    ent_addAgendaDate.grid(column=2, row=1, columnspan=2, sticky="w")
    lbl_addAgendaDateNote.grid(column=2, row=2, columnspan=2, sticky="w")
    lbl_addAgendaNum.grid(column=1, row=3, padx=40, sticky="w")
    ent_addAgendaNum.grid(column=2, row=3, columnspan=2, pady=10, sticky="w")
    lbl_addAgendaCategory.grid(column=1, row=5, padx=40, sticky="w")
    btn_addAgendaPersonal.grid(column=2, row=5, pady=10, sticky="w")
    btn_addAgendaGrup.grid(column=3, row=5, pady=10, sticky="w")
    btn_addAgendaSubmit.grid(column=1, row=8, columnspan=3, pady=5) 
    frm_addAgenda.grid(column=0, row=1, sticky="ensw")
    frm_addAgenda.rowconfigure([0,9], weight=1)
    frm_addAgenda.columnconfigure([0,4], weight=1) 

# SUBMIT ADD MEMBER
def submitmem():
    global payload
    global memberListNew

    memberList = ""
    

    for entries in members:
        if str(entries.get())=="":
            addMemberInvalid = Label(frm_AMsubmit, text="Invalid! Masukkan seluruh member!\natau ubah jumlah member", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="center")
            addMemberInvalid.grid(column=0, row=0, columnspan=3, sticky="news")
            invalid = 1
            break
        else:
            memberList = memberList + str(entries.get()) + ","

            memberListNew = memberList.rstrip(",")  
            invalid = 0

    if invalid == 1:
        pop_addMember.mainloop()
    else:    
        pop_addMember.destroy()

# submit add member
def submitAG(token):
    groupNum=AGNum.get()

    valid=0

    if groupNum == "0":
        lbl_addGroupNumInvalid = Label(frm_addGroup, text="Invalid! Masukkan jumlah anggota!", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_addGroupNumInvalid.grid(column=2, row=4, padx=40, sticky="ew")
        print("Jumlah Anggota Invalid!")
    else:
        lbl_addAgendaNumInvalid = Label(frm_addGroup, text="Ok", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_addAgendaNumInvalid.grid(column=2, row=4, padx=40, sticky="ew")  
        print("Jumlah Anggota Valid!")
        valid = valid + 1  


    gn = ent_addGroupName.get()

    # validating group name
    regexgn = "^[^-\s]{5,45}$"
    # tidak ada spasi
    # antara 5 sampai 45 huruf
    # compiling regex
    patgn = re.compile(regexgn)
    # searching regex                 
    matgn = re.search(patgn, gn)

    if matgn: 
        print("Valid Group Name")
        valid = valid + 1
        lbl_addAgendaGroupNameInvalid = Label(frm_addGroup, text="Ok", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_addAgendaGroupNameInvalid.grid(column=2, row=2, padx=40, sticky="we")
    else:
        print("Group Name Invalid!!") 
        lbl_addAgendaGroupNameInvalid = Label(frm_addGroup, text="Invalid! Nama grup 5-45 huruf, tanpa spasi", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_addAgendaGroupNameInvalid.grid(column=2, row=2, padx=40, sticky="we")

    if valid == 2:
        post = requests.post(urlAddGroup,data={"nama_grup": gn, "username": memberListNew},headers={"x-access-token": token})
        print(post)
        print(post.text)
        if(post.text == "{\"message\":\"Failed! Group name is already in use!\"}"):
            print("Group Name is already in use!")
            lbl_addAgendaGroupNameInvalid = Label(frm_addGroup, text="Group Name is already in use!", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
            lbl_addAgendaGroupNameInvalid.grid(column=2, row=2, padx=40, sticky="we")
            pop_addGroup.mainloop()
        else:
            pop_addGroup.destroy()       
    else:
        pop_addGroup.mainloop()    

# FORM ADD MEMBER
def addMember(token):
    groupNum = AGNum.get()    


    global pop_addMember
    global members
    global frm_addMember
    global frm_AMsubmit


    if groupNum == 0:
        lbl_addGroupNumInvalid = Label(frm_addMember, text="Mohon pilih jumlah anggota", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")  
        lbl_addGroupNumInvalid.grid(column=2, row=4, padx=40, sticky="we")
        addGroup(token)
    else:
        members = []

        pop_addMember = Toplevel(homePg)
        pop_addMember.title("ToDoList-Add Member")
        pop_addMember.rowconfigure(1, weight=1)
        pop_addMember.columnconfigure(0, weight=1)
        pop_addMember.minsize(500,230)
        pop_addMember.maxsize(500,230)
        centered (pop_addMember, 500, 230)


        # add member Form - Header
        lbl_headeraddMember = Label(pop_addMember, text="Menambah Anggota", bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

        lbl_headeraddMember.grid(column=0, row=0, sticky="ensw")

        frm_mcanvas = Frame(pop_addMember)
        frm_mcanvas.grid(column=0, row=1, sticky="news")
        frm_mcanvas.rowconfigure(0, weight=1)
        frm_mcanvas.columnconfigure(0, weight=1)        
        frm_AMsubmit = Frame(pop_addMember, bg="#FFFFFF")
        frm_AMsubmit.grid(column=0, row=2, sticky="news")
        frm_AMsubmit.rowconfigure(0, weight=1)
        frm_AMsubmit.columnconfigure(0, weight=1)        
        
    
        frm_mcanvas.grid_propagate(False)

        mcanvas = Canvas(frm_mcanvas)
        mcanvas.grid(column=0, row=0, sticky="news")

        mscrollbar=Scrollbar(frm_mcanvas, orient="vertical", command=mcanvas.yview)
        mscrollbar.grid(column=1, row=0, sticky="ns")
        mcanvas.configure(yscrollcommand=mscrollbar.set)    

        # add member form body
        frm_addMember = Frame(mcanvas, bg="#FFFFFF")    
        mcanvas.create_window((0,0), window=frm_addMember, anchor="nw")
        lbl_addMemberSpaceN = Label(frm_addMember, bg="#FFFFFF")
        lbl_addMemberSpaceS = Label(frm_addMember, bg="#FFFFFF")
        lbl_addMemberSpaceW = Label(frm_addMember, bg="#FFFFFF")
        lbl_addMemberSpaceE = Label(frm_addMember, bg="#FFFFFF")
        


        for i in range(int(groupNum)): 
            lbl_addMember = Label(frm_addMember, text=f"Anggota ke-{i+1}", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
            ent_addMember = Entry(frm_addMember, text="", width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000")
            lbl_addMember.grid(column=1, row=1+(i+1), padx=40, sticky="w",pady=5)
            ent_addMember.grid(column=2, row=1+(i+1),  columnspan=2,  padx=40, pady=10, sticky="w")
            members.append(ent_addMember)

    
        lbl_addMemberSpaceN.grid(column=0, row=0, columnspan=4)
        lbl_addMemberSpaceS.grid(column=0, row=int(groupNum)+3, columnspan=4)
        lbl_addMemberSpaceW.grid(column=0, row=1, rowspan=int(groupNum)+3)
        lbl_addMemberSpaceE.grid(column=4, row=1, rowspan=int(groupNum)+3)
        frm_addMember.update_idletasks()        

        btn_AMSubmit = Button(frm_AMsubmit, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=submitmem)
        btn_AMSubmit.grid(column=0, row=1, columnspan=3, sticky="news", pady=5) 
        mcanvas.config(scrollregion=mcanvas.bbox("all"))    


        frm_mcanvas.config(width=500 + mscrollbar.winfo_width(),height=230)     
        frm_addMember.rowconfigure([0,(int(groupNum)+2)], weight=1)
        frm_addMember.columnconfigure([0,5], weight=1)  

#FORM ADD GROUP
def addGroup(token):
    global frm_addGroup
    global pop_addGroup
    global ent_addGroupName

    pop_addGroup = Toplevel(homePg)
    pop_addGroup.title("ToDoList-Add Group")
    pop_addGroup.rowconfigure(1, weight=1)
    pop_addGroup.columnconfigure(0, weight=1)
    pop_addGroup.minsize(500,230)
    centered (pop_addGroup, 500, 230)

    global AGNum
    AGNum = StringVar(pop_addGroup)
    AGNum.set(0)

    # add group Form - Header
    lbl_addGroupHeader = Label(pop_addGroup, text="Menambah Group", bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

    lbl_addGroupHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")

    # add group form body
    global frm_addGroup  

    frm_addGroup = Frame(pop_addGroup, bg="#FFFFFF")
    lbl_addGroupSpaceN = Label(frm_addGroup, bg="#FFFFFF")
    lbl_addGroupSpaceS = Label(frm_addGroup, bg="#FFFFFF")
    lbl_addGroupSpaceW = Label(frm_addGroup, bg="#FFFFFF")
    lbl_addGroupSpaceE = Label(frm_addGroup, bg="#FFFFFF")
    lbl_addGroupName = Label(frm_addGroup, text="Nama Grup", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_addGroupName = Entry(frm_addGroup,  text="", width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000")
    lbl_addGroupNum = Label(frm_addGroup, text="Jumlah Anggota", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_addGroupNum = ttk.Combobox(frm_addGroup,  width=10, textvariable=AGNum, values=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100], font=("OpenSans", 10))
    ent_addGroupNum.bind("<<ComboboxSelected>>", lambda event: addMember(token))  
    btn_addGroupSubmit = Button(frm_addGroup, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=lambda:submitAG(token))
    
    lbl_addGroupSpaceN.grid(column=0, row=0, columnspan=4)
    lbl_addGroupSpaceS.grid(column=0, row=6, columnspan=4)
    lbl_addGroupSpaceW.grid(column=0, row=1, rowspan=5)
    lbl_addGroupSpaceE.grid(column=3, row=1, rowspan=5)
    lbl_addGroupName.grid(column=1, row=1, padx=40, sticky="w")
    ent_addGroupName.grid(column=2, row=1, padx=40, sticky="w")
    lbl_addGroupNum.grid(column=1, row=3, padx=40, sticky="w")
    ent_addGroupNum.grid(column=2, row=3, padx=40, pady=10, sticky="w")
    btn_addGroupSubmit.grid(column=1, row=5, columnspan=2, pady=5) 
    frm_addGroup.grid(column=0, row=1, sticky="ensw")
    frm_addGroup.rowconfigure([0,6], weight=1)
    frm_addGroup.columnconfigure([0,3], weight=1)      

def logout():
    pop_dashBoard.destroy()    

def dashBoardMABack(username,token):
    pop_dashBoardMA.destroy()
    dashBoard(username,token)

# DASHBOARD MANAGE AGENDA
def dashBoardMA(username,token):
    pop_dashBoard.destroy()
    global pop_dashBoardMA
    pop_dashBoardMA = Toplevel(homePg)
    pop_dashBoardMA.title("ToDoList-Mengelola Agenda")
    pop_dashBoardMA.rowconfigure(1, weight=1)
    pop_dashBoardMA.columnconfigure(0, weight=1)
    pop_dashBoardMA.minsize(1150,600)
    centered (pop_dashBoardMA, 1150, 600)

    # Header
    frm_dashBoardMAHeader = Frame(pop_dashBoardMA, bg="#000000")
    lbl_dashBoardMATitle = Label(frm_dashBoardMAHeader, bg="#000000", image=photo_lgHeader, borderwidth=0)
    lbl_dashBoardMAPP = Label(frm_dashBoardMAHeader, bg="#2D2D2D", fg="#FFFFFF", text=username, font=("OpenSans",10,'bold'), anchor="e", image=photo_PP, compound=LEFT, padx=10)

    lbl_dashBoardMATitle.grid(column=0, row=0, sticky="w")
    lbl_dashBoardMAPP.grid(column=1, row=0, sticky="e")
    frm_dashBoardMAHeader.grid(column=0, row=0, sticky="ensw")
    frm_dashBoardMAHeader.columnconfigure([0,1], weight=1)

    # Body
    # Body - title
    frm_dashBoardMABody = Frame(pop_dashBoardMA, bg="#FFFFFF", padx=5)
    lbl_dashBoardMABodySpaceN = Label(frm_dashBoardMABody, bg="#FFFFFF")
    lbl_dashBoardMABodySpaceS = Label(frm_dashBoardMABody, bg="#FFFFFF")
    lbl_dashBoardMABodySpaceW = Label(frm_dashBoardMABody, bg="#FFFFFF")
    lbl_dashBoardMABodySpaceE = Label(frm_dashBoardMABody, bg="#FFFFFF")
    lbl_dashBoardMABodyTitle = Label(frm_dashBoardMABody, bg="#FFFFFF", text="Mengelola Agenda", font=("OpenSans",15,'bold'))
    lbl_dashBoardMABodyTitleLine = Label(frm_dashBoardMABody, bg="#FFFFFF", image=photo_lnBodyTitle,  borderwidth=0)
    btn_dashBoardMAlogout = Button(frm_dashBoardMABody, bg="#FFFFFF", image=photo_btnBack, cursor="hand2",  borderwidth=0, command=lambda: dashBoardMABack(username,token))
    
    frm_dashBoardMAAddAgenda = Frame(frm_dashBoardMABody, bg="#FFFFFF", padx=10, pady=10, highlightbackground="#CACACA", highlightthickness=1)
    lbl_dashBoardMAAANum = Label(frm_dashBoardMAAddAgenda, bg="#FFFFFF", image=photo_1)
    lbl_dashBoardMAAAIcon = Label(frm_dashBoardMAAddAgenda, bg="#FFFFFF", image=photo_AAicon)
    btn_dashBoardMAAA = Button(frm_dashBoardMAAddAgenda, bg="#FFFFFF", image=photo_btnAA, cursor="hand2",  borderwidth=0, pady=10, command=lambda: addAgenda(username,token))

    frm_dashBoardMASeeAgenda = Frame(frm_dashBoardMABody, bg="#FFFFFF", padx=10, pady=10, highlightbackground="#CACACA", highlightthickness=1)
    lbl_dashBoardMAVANum = Label(frm_dashBoardMASeeAgenda, bg="#FFFFFF", image=photo_2)
    lbl_dashBoardMAVAIcon = Label(frm_dashBoardMASeeAgenda, bg="#FFFFFF", image=photo_VAicon)
    btn_dashBoardMAVA = Button(frm_dashBoardMASeeAgenda, bg="#FFFFFF", image=photo_btnVA, cursor="hand2",  borderwidth=0,  pady=10, command=lambda: seeAgenda(username, token))

    frm_dashBoardMADelAgenda = Frame(frm_dashBoardMABody, bg="#FFFFFF", padx=10, pady=10, highlightbackground="#CACACA", highlightthickness=1)
    lbl_dashBoardMADANum = Label(frm_dashBoardMADelAgenda, bg="#FFFFFF", image=photo_3)
    lbl_dashBoardMADAIcon = Label(frm_dashBoardMADelAgenda, bg="#FFFFFF", image=photo_DAicon)
    btn_dashBoardMADA = Button(frm_dashBoardMADelAgenda, bg="#FFFFFF", image=photo_btnDA, cursor="hand2",  borderwidth=0,  pady=10, command=lambda: delAgenda(username, token))

    lbl_dashBoardMABodySpaceN.grid(column=1, row=0, columnspan=3)
    lbl_dashBoardMABodySpaceS.grid(column=1, row=5, columnspan=3)
    lbl_dashBoardMABodySpaceW.grid(column=0, row=0, rowspan=6, sticky = "s")
    lbl_dashBoardMABodySpaceE.grid(column=4, row=0, rowspan=6, sticky = "s")
    lbl_dashBoardMABodyTitle.grid(column=1, row=1, columnspan=3)
    lbl_dashBoardMABodyTitleLine.grid(column=1, row=2, columnspan=3)
    btn_dashBoardMAlogout.grid(column=1, row=4, columnspan=3, pady=10, padx=5)

    frm_dashBoardMAAddAgenda.grid(column=1, row=3, padx=10, pady=30)
    lbl_dashBoardMAAANum.grid(column=0, row=0, sticky="nw")
    lbl_dashBoardMAAAIcon.grid(column=0, row=1, columnspan=2, sticky="we")
    btn_dashBoardMAAA.grid(column=0, row=2, columnspan=2, sticky="ensw", pady=10)

    frm_dashBoardMASeeAgenda.grid(column=2, row=3, padx=10, pady=10)
    lbl_dashBoardMAVANum.grid(column=0, row=0, sticky="nw")
    lbl_dashBoardMAVAIcon.grid(column=0, row=1, columnspan=2,  sticky="we")
    btn_dashBoardMAVA.grid(column=0, row=2, columnspan=2, sticky="ensw", pady=10)    

    frm_dashBoardMADelAgenda.grid(column=3, row=3, padx=10, pady=10)
    lbl_dashBoardMADANum.grid(column=0, row=0, sticky="nw")
    lbl_dashBoardMADAIcon.grid(column=0, row=1, columnspan=2,  sticky="we")
    btn_dashBoardMADA.grid(column=0, row=2, columnspan=2, sticky="ensw", pady=10)    

    frm_dashBoardMABody.grid(column=0, row=1, sticky="ensw")
    frm_dashBoardMABody.rowconfigure([0,5], weight=1)
    frm_dashBoardMABody.columnconfigure([0,4], weight=1)

    # Footer
    frm_dashBoardMAFooter = Frame(pop_dashBoardMA, bg="#000000")
    lbl_dashBoardMAFooterSpaceN = Label(frm_dashBoardMAFooter, bg="#000000")
    lbl_dashBoardMAFooterSpaceS = Label(frm_dashBoardMAFooter, bg="#000000")
    lbl_dashBoardMAFooterSpaceW = Label(frm_dashBoardMAFooter, bg="#000000")
    lbl_dashBoardMAFooterSpaceE = Label(frm_dashBoardMAFooter, bg="#000000")
    lbl_dashBoardMAFooterCP = Label(frm_dashBoardMAFooter, bg="#000000", fg="#FFFFFF", text="Hubungi Kami", font=("OpenSans", 8), anchor="e")
    lbl_dashBoardMAFooterLine = Label(frm_dashBoardMAFooter, bg="#FFFFFF", padx=0.1)
    btn_dashBoardMAFooterIg = Button(frm_dashBoardMAFooter, bg="#000000", image=photo_btnIg, cursor="hand2",  borderwidth=0)
    btn_dashBoardMAFooterWA = Button(frm_dashBoardMAFooter, bg="#000000", image=photo_btnWA, cursor="hand2",  borderwidth=0)
    btn_dashBoardMAFooterMail = Button(frm_dashBoardMAFooter, bg="#000000", image=photo_btnMail, cursor="hand2",  borderwidth=0)
    btn_dashBoardMAFooterSK = Button(frm_dashBoardMAFooter, bg="#000000", fg="#FFFFFF", text="Syarat Ketentuan", font=("OpenSans", 8), cursor="hand2",  borderwidth=0, anchor="w")
    btn_dashBoardMAFooterKP = Button(frm_dashBoardMAFooter, bg="#000000", fg="#FFFFFF", text="Kebijakan Privasi", font=("OpenSans", 8), cursor="hand2",  borderwidth=0, anchor="w")

    lbl_dashBoardMAFooterSpaceN.grid(column=0, row=0, columnspan=7, pady=3)
    lbl_dashBoardMAFooterSpaceS.grid(column=0, row=3, columnspan=7, pady=3)
    lbl_dashBoardMAFooterSpaceW.grid(column=0, row=1, rowspan=2, padx=10)
    lbl_dashBoardMAFooterSpaceE.grid(column=6, row=1, rowspan=2, padx=10)
    lbl_dashBoardMAFooterCP.grid(column=1, row=1, columnspan=3, sticky="ensw")
    lbl_dashBoardMAFooterLine.grid(column=4, row=1, rowspan=2, sticky="ensw", padx=20)
    btn_dashBoardMAFooterIg.grid(column=1, row=2, pady=5, padx=5)
    btn_dashBoardMAFooterWA.grid(column=2, row=2, padx=5)
    btn_dashBoardMAFooterMail.grid(column=3, row=2, padx=5)
    btn_dashBoardMAFooterSK.grid(column=5, row=1)
    btn_dashBoardMAFooterKP.grid(column=5, row=2)
    frm_dashBoardMAFooter.grid(column=0, row=2, sticky="ensw")
    frm_dashBoardMAFooter.columnconfigure([0,7], weight=1)

# DASHBOARD
def dashBoard(username,token):
    global pop_dashBoard
    pop_dashBoard = Toplevel(homePg)
    pop_dashBoard.title("ToDoList-Dashboard")
    pop_dashBoard.rowconfigure(1, weight=1)
    pop_dashBoard.columnconfigure(0, weight=1)
    pop_dashBoard.minsize(1150,600)
    centered (pop_dashBoard, 1150, 600)

    # Header  
    frm_dashBoardHeader = Frame(pop_dashBoard, bg="#000000")
    lbl_dashBoardTitle = Label(frm_dashBoardHeader, bg="#000000", image=photo_lgHeader, borderwidth=0)
    lbl_dashBoardPP = Label(frm_dashBoardHeader, bg="#2D2D2D", fg="#FFFFFF", text=username, font=("OpenSans",10,'bold'), anchor="e", image=photo_PP, compound=LEFT, padx=10)

    lbl_dashBoardTitle.grid(column=0, row=0, sticky="w")
    lbl_dashBoardPP.grid(column=1, row=0, sticky="e")
    frm_dashBoardHeader.grid(column=0, row=0, sticky="ensw")
    frm_dashBoardHeader.columnconfigure([0,1], weight=1)

    # Body
    # Body - title
    frm_dashBoardBody = Frame(pop_dashBoard, bg="#FFFFFF", padx=5)
    lbl_dashBoardBodySpaceN = Label(frm_dashBoardBody, bg="#FFFFFF")
    lbl_dashBoardBodySpaceS = Label(frm_dashBoardBody, bg="#FFFFFF")
    lbl_dashBoardBodySpaceW = Label(frm_dashBoardBody, bg="#FFFFFF")
    lbl_dashBoardBodySpaceE = Label(frm_dashBoardBody, bg="#FFFFFF")
    lbl_dashBoardBodyTitle = Label(frm_dashBoardBody, bg="#FFFFFF", text="Dashboard", font=("OpenSans",15,'bold'))
    lbl_dashBoardBodyTitleLine = Label(frm_dashBoardBody, bg="#FFFFFF", image=photo_lnBodyTitle,  borderwidth=0)
    btn_dashBoardlogout = Button(frm_dashBoardBody, bg="#FFFFFF", image=photo_btnLogout, cursor="hand2",  borderwidth=0, command=logout)

    frm_dashBoardManAgenda = Frame(frm_dashBoardBody, bg="#FFFFFF", padx=10, pady=10, highlightbackground="#CACACA", highlightthickness=1)
    lbl_dashBoardMANum = Label(frm_dashBoardManAgenda, bg="#FFFFFF", image=photo_1)
    lbl_dashBoardMAIcon = Label(frm_dashBoardManAgenda, bg="#FFFFFF", image=photo_MAicon)
    btn_dashBoardMA = Button(frm_dashBoardManAgenda, bg="#FFFFFF", image=photo_btnMA, cursor="hand2",  borderwidth=0, pady=10, command=lambda:dashBoardMA(username, token))

    frm_dashBoardAddGroup = Frame(frm_dashBoardBody, bg="#FFFFFF", padx=10, pady=10, highlightbackground="#CACACA", highlightthickness=1)
    lbl_dashBoardAGNum = Label(frm_dashBoardAddGroup, bg="#FFFFFF", image=photo_2)
    lbl_dashBoardAGIcon = Label(frm_dashBoardAddGroup, bg="#FFFFFF", image=photo_AGicon)
    btn_dashBoardAG = Button(frm_dashBoardAddGroup, bg="#FFFFFF", image=photo_btnAG, cursor="hand2",  borderwidth=0,  pady=10, command=lambda: addGroup(token))

    frm_dashBoardCalendar = Frame(frm_dashBoardBody, bg="#FFFFFF", padx=10, pady=10, highlightbackground="#CACACA", highlightthickness=1)
    cal_dashBoardCalendar = Calendar(
        frm_dashBoardCalendar, 
        font=("Opensans", 10, "bold"),
        selectmode="day", 
        firstweekday="sunday", 
        background="#FFFFFF", 
        foreground="#000000", 
        disabledforeground="#DDDDDD", 
        bordercolor="#FFFFFF", 
        normalbackground="#FFFFFF", 
        weekendbackground="#FFFFFF", 
        weekendforeground ="#000000", 
        disabledbackground="99b3bc",
        headersbackground="#000000", 
        headersforeground="#FFFFFF",
        selectbackground="#000000",
        selectforeground="#FFFFFF",
        othermonthforeground="#AAAAAA",
        othermonthbackground="#FFFFFF",
        othermonthweforeground="#AAAAAA",
        othermonthwebackground="#FFFFFF",
        disableddaybackground="#FFFFFF",
        disableddayforeground="#DDDDDD",
        cursor="hand2",
        year=int(datetime.datetime.now().strftime("%Y")), month=int(datetime.datetime.now().strftime("%m")), day=int(datetime.datetime.now().strftime("%d")))


    def submitSAC():
        global frm_viewAgendaCal
        global pop_viewAgendaCal
        
        pop_viewAgendaCal = Toplevel(homePg)
        pop_viewAgendaCal.title("ToDoList-view")
        pop_viewAgendaCal.rowconfigure(1, weight=1)
        pop_viewAgendaCal.columnconfigure(0, weight=1)
        pop_viewAgendaCal.minsize(500,230)
        centered (pop_viewAgendaCal, 500, 230)

        activityDate = cal_dashBoardCalendar.selection_get()
        activityDateFormatted = activityDate.strftime("%d/%m/%Y")

        # Get agenda by personal or group
        payload = {}
        categoryValue = calCategoryVar.get()
        if categoryValue == 1:
            payload['kategori'] = "PERSONAL"
        else:
            #prepare payload
            groupName = ent_seeAgendaGroupNameCal.get()
            payload['kategori'] = "GRUP"
            payload['nama_grup'] = groupName
            # Send get request to retrieve group member by group name
            dataAngggota = requests.get(urlGetGroupMember, data= {"nama_grup":groupName }, headers={"x-access-token": token}).json()
            listAnggota = ""
            for anggota in dataAngggota['member']:
                if anggota == dataAngggota['member'][-1]:
                    listAnggota += anggota['username']
                else:
                    listAnggota += anggota['username'] + ', '

        payload['username'] = username
        payload['tanggal'] = activityDate.strftime("%Y-%m-%d")
        
        # Send get request to retrieve activity by payload
        data = requests.get(urlViewActivity, data=payload, headers={"x-access-token": token}).json()

        listKegiatan = []
        if "kegiatan" in data:
            for kegiatan in data['kegiatan']:
                listKegiatan.insert(1, kegiatan['kegiatan'])


        # view agenda Form - Header
        lbl_viewAgendaHeader = Label(pop_viewAgendaCal, text="Agenda " + activityDateFormatted, bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

        lbl_viewAgendaHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")
        
        # view agenda form body
        global frm_viewAgendaCal 
        frm_viewAgendaCal = Frame(pop_viewAgendaCal, bg="#FFFFFF")
        lbl_viewAgendaCalSpaceN = Label(frm_viewAgendaCal, bg="#FFFFFF")
        lbl_viewAgendaCalSpaceS = Label(frm_viewAgendaCal, bg="#FFFFFF")
        lbl_viewAgendaCalSpaceW = Label(frm_viewAgendaCal, bg="#FFFFFF")
        lbl_viewAgendaCalSpaceE = Label(frm_viewAgendaCal, bg="#FFFFFF")
        lbl_viewAgendaCalKategori = Label(frm_viewAgendaCal, text="Kategori:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        categoryValue = calCategoryVar.get()
        if categoryValue == 1:
            lbl_viewAgendaCalKategori1 = Label(frm_viewAgendaCal, text="Personal", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        else:
            lbl_viewAgendaCalKategori1 = Label(frm_viewAgendaCal, text="Grup", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        lbl_viewAgendaCalKegiatan = Label(frm_viewAgendaCal, text="Kegiatan:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        btn_viewAgendaCalDone = Button(frm_viewAgendaCal, bg="#FFFFFF", image=photo_btnDone, cursor="hand2",  borderwidth=0, command=SACdone)

        lbl_listAgendaKegiatan = Text(frm_viewAgendaCal, bg="#FFFFFF", font=("OpenSans",10), borderwidth=0, height=5 , yscrollcommand =True)

        if categoryValue == 2:
            lbl_viewAgendaNamaGrup = Label(frm_viewAgendaCal, text="Nama Grup:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
            lbl_viewAgendaNamaGrupData = Label(frm_viewAgendaCal, text=groupName, bg="#FFFFFF", font=("OpenSans",10), anchor="w")
            lbl_viewAgendaNamaGrup.grid(column=1, row=2, padx=40, sticky="w")
            lbl_viewAgendaNamaGrupData.grid(column=2, row=2, padx=40, sticky="w")

            lbl_viewAgendaAnggota = Label(frm_viewAgendaCal, text="Anggota:", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
            lbl_viewAgendaAnggotaList = Label(frm_viewAgendaCal, text=listAnggota, bg="#FFFFFF", font=("OpenSans",10), anchor="w")
            lbl_viewAgendaAnggota.grid(column=1, row=3, padx=40, sticky="w")
            lbl_viewAgendaAnggotaList.grid(column=2, row=3, padx=40, sticky="w")

        if listKegiatan:
            for index,kegiatan in enumerate(listKegiatan):
                lbl_listAgendaKegiatan.insert(END, str(index+1) + ". " +kegiatan + '\n')
        else:
            lbl_listAgendaKegiatan.insert(END, "Tidak ada kegiatan.")
        lbl_listAgendaKegiatan.configure(state="disabled")
        
        lbl_viewAgendaCalSpaceN.grid(column=0, row=0, columnspan=4)
        lbl_viewAgendaCalSpaceS.grid(column=0, row=6, columnspan=4)
        lbl_viewAgendaCalSpaceW.grid(column=0, row=1, rowspan=5)
        lbl_viewAgendaCalSpaceE.grid(column=3, row=1, rowspan=5)
        lbl_viewAgendaCalKategori.grid(column=1, row=1, padx=40, sticky="w")
        lbl_viewAgendaCalKategori1.grid(column=2, row=1, padx=40, sticky="w")
        lbl_viewAgendaCalKegiatan.grid(column=1, row=4, padx=40, sticky="n")
        lbl_listAgendaKegiatan.grid(column=2, row=4, padx=40, sticky="w")
        btn_viewAgendaCalDone.grid(column=1, row=6, columnspan=2, pady=5) 
        frm_viewAgendaCal.grid(column=0, row=1, sticky="ensw")
        frm_viewAgendaCal.rowconfigure([0,6], weight=1)
        frm_viewAgendaCal.columnconfigure([0,3], weight=1)  

    def seeAgendaCal(event):
        global frm_seeAgendaCal
        global pop_seeAgendaCal

        pop_seeAgendaCal = Toplevel(homePg)
        pop_seeAgendaCal.title("ToDoList-View Agenda Calendar")
        pop_seeAgendaCal.rowconfigure(1, weight=1)
        pop_seeAgendaCal.columnconfigure(0, weight=1)
        pop_seeAgendaCal.minsize(500,230)
        centered (pop_seeAgendaCal, 500, 230)

        global calCategoryVar
        calCategoryVar=IntVar()
        calCategoryVar.set(1)

        activityDate = cal_dashBoardCalendar.selection_get()
        
        activityDateFormatted = activityDate.strftime("%d/%m/%Y")

        # see agenda Form - Header
        lbl_seeAgendaCalHeader = Label(pop_seeAgendaCal, text="Agenda " + activityDateFormatted, bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

        lbl_seeAgendaCalHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")

        # see agenda form body
        global frm_seeAgendaCal   
        frm_seeAgendaCal = Frame(pop_seeAgendaCal, bg="#FFFFFF")
        lbl_seeAgendaCalSpaceN = Label(frm_seeAgendaCal, bg="#FFFFFF")
        lbl_seeAgendaCalSpaceS = Label(frm_seeAgendaCal, bg="#FFFFFF")
        lbl_seeAgendaCalSpaceW = Label(frm_seeAgendaCal, bg="#FFFFFF")
        lbl_seeAgendaCalSpaceE = Label(frm_seeAgendaCal, bg="#FFFFFF")
        lbl_seeAgendaCalCategory = Label(frm_seeAgendaCal, text="Kategori", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
        btn_seeAgendaCalPersonal = Radiobutton(frm_seeAgendaCal, bg="#FFFFFF", activebackground="#000000", activeforeground="#FFFFFF",text="Personal", cursor="hand2",  borderwidth=1, variable=calCategoryVar, value=1, command=lambda :inputGroupNameSAC(1))
        btn_seeAgendaCalGrup = Radiobutton(frm_seeAgendaCal, bg="#FFFFFF", activebackground="#000000", activeforeground="#FFFFFF", text="Grup", cursor="hand2",  borderwidth=1, variable=calCategoryVar, value=2, command=lambda: inputGroupNameSAC(2))
        btn_seeAgendaCalSubmit = Button(frm_seeAgendaCal, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=submitSAC)
        
        lbl_seeAgendaCalSpaceN.grid(column=0, row=0, columnspan=5)
        lbl_seeAgendaCalSpaceS.grid(column=0, row=7, columnspan=5)
        lbl_seeAgendaCalSpaceW.grid(column=0, row=1, rowspan=7)
        lbl_seeAgendaCalSpaceE.grid(column=3, row=1, rowspan=7, padx=20)
        lbl_seeAgendaCalCategory.grid(column=1, row=2, padx=40, sticky="w")
        btn_seeAgendaCalPersonal.grid(column=2, row=2, pady=10, sticky="w")
        btn_seeAgendaCalGrup.grid(column=3, row=2, pady=10, sticky="w")
        btn_seeAgendaCalSubmit.grid(column=1, row=5, columnspan=3, pady=5) 
        frm_seeAgendaCal.grid(column=0, row=1, sticky="ensw")
        frm_seeAgendaCal.rowconfigure([0,5], weight=1)
        frm_seeAgendaCal.columnconfigure([0,4], weight=1) 

    cal_dashBoardCalendar.bind("<<CalendarSelected>>", seeAgendaCal)

    lbl_dashBoardBodySpaceN.grid(column=1, row=0, columnspan=3)
    lbl_dashBoardBodySpaceS.grid(column=1, row=5, columnspan=3)
    lbl_dashBoardBodySpaceW.grid(column=0, row=0, rowspan=6, sticky = "s")
    lbl_dashBoardBodySpaceE.grid(column=4, row=0, rowspan=6, sticky = "s")
    lbl_dashBoardBodyTitle.grid(column=1, row=1, columnspan=3)
    lbl_dashBoardBodyTitleLine.grid(column=1, row=2, columnspan=3)
    btn_dashBoardlogout.grid(column=1, row=4, columnspan=3, pady=10, padx=5)

    frm_dashBoardManAgenda.grid(column=1, row=3, padx=10)
    lbl_dashBoardMANum.grid(column=0, row=0, sticky="nw")
    lbl_dashBoardMAIcon.grid(column=0, row=1, columnspan=2, sticky="we")
    btn_dashBoardMA.grid(column=0, row=2, columnspan=2, sticky="ensw", pady=10)

    frm_dashBoardAddGroup.grid(column=2, row=3, padx=10, pady=30)
    lbl_dashBoardAGNum.grid(column=0, row=0, sticky="nw")
    lbl_dashBoardAGIcon.grid(column=0, row=1, columnspan=2, sticky="we")
    btn_dashBoardAG.grid(column=0, row=2, columnspan=2, sticky="ensw", pady=10)    

    frm_dashBoardCalendar.grid(column=3, row=3, padx=10)
    cal_dashBoardCalendar.grid(column=0, row=0)

    frm_dashBoardBody.grid(column=0, row=1, sticky="ensw")
    frm_dashBoardBody.rowconfigure([0,5], weight=1)
    frm_dashBoardBody.columnconfigure([0,4], weight=1)

    # Footer
    frm_dashBoardFooter = Frame(pop_dashBoard, bg="#000000")
    lbl_dashBoardFooterSpaceN = Label(frm_dashBoardFooter, bg="#000000")
    lbl_dashBoardFooterSpaceS = Label(frm_dashBoardFooter, bg="#000000")
    lbl_dashBoardFooterSpaceW = Label(frm_dashBoardFooter, bg="#000000")
    lbl_dashBoardFooterSpaceE = Label(frm_dashBoardFooter, bg="#000000")
    lbl_dashBoardFooterCP = Label(frm_dashBoardFooter, bg="#000000", fg="#FFFFFF", text="Hubungi Kami", font=("OpenSans", 8), anchor="e")
    lbl_dashBoardFooterLine = Label(frm_dashBoardFooter, bg="#FFFFFF", padx=0.1)
    btn_dashBoardFooterIg = Button(frm_dashBoardFooter, bg="#000000", image=photo_btnIg, cursor="hand2",  borderwidth=0)
    btn_dashBoardFooterWA = Button(frm_dashBoardFooter, bg="#000000", image=photo_btnWA, cursor="hand2",  borderwidth=0)
    btn_dashBoardFooterMail = Button(frm_dashBoardFooter, bg="#000000", image=photo_btnMail, cursor="hand2",  borderwidth=0)
    btn_dashBoardFooterSK = Button(frm_dashBoardFooter, bg="#000000", fg="#FFFFFF", text="Syarat Ketentuan", font=("OpenSans", 8), cursor="hand2",  borderwidth=0, anchor="w")
    btn_dashBoardFooterKP = Button(frm_dashBoardFooter, bg="#000000", fg="#FFFFFF", text="Kebijakan Privasi", font=("OpenSans", 8), cursor="hand2",  borderwidth=0, anchor="w")

    lbl_dashBoardFooterSpaceN.grid(column=0, row=0, columnspan=7, pady=3)
    lbl_dashBoardFooterSpaceS.grid(column=0, row=3, columnspan=7, pady=3)
    lbl_dashBoardFooterSpaceW.grid(column=0, row=1, rowspan=2, padx=10)
    lbl_dashBoardFooterSpaceE.grid(column=6, row=1, rowspan=2, padx=10)
    lbl_dashBoardFooterCP.grid(column=1, row=1, columnspan=3, sticky="ensw")
    lbl_dashBoardFooterLine.grid(column=4, row=1, rowspan=2, sticky="ensw", padx=20)
    btn_dashBoardFooterIg.grid(column=1, row=2, pady=5, padx=5)
    btn_dashBoardFooterWA.grid(column=2, row=2, padx=5)
    btn_dashBoardFooterMail.grid(column=3, row=2, padx=5)
    btn_dashBoardFooterSK.grid(column=5, row=1)
    btn_dashBoardFooterKP.grid(column=5, row=2)
    frm_dashBoardFooter.grid(column=0, row=2, sticky="ensw")
    frm_dashBoardFooter.columnconfigure([0,7], weight=1)


# REGISTRATION FORM SUBMIT
def regFormSubmit():
    global username
    global password
    global email
    global passwordConfirm
    global valid
    global payload
    global lbl_rfBodyUnameInvalid
    global lbl_rfBodyEmailInvalid
    global lbl_rfBodyPassInvalid
    username = ent_rfBodyUname.get()
    password = ent_rfBodyPass.get()
    passwordConfirm = ent_rfBodyPassConfirm.get()
    email = ent_rfBodyEmail.get()
    valid=0

    # validating username
    regexU = "^[^-\s]{8,45}$"
    # tanpa spasi
    # antara 8 sampai 45 huruf
    # compiling regex
    patU = re.compile(regexU)
    # searching regex                 
    matU = re.search(patU, username)

    if matU: 
        print("Valid Username")
        valid = valid + 1
        lbl_rfBodyUnameInvalid = Label(frm_regBody, text="Username anda Valid", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_rfBodyUnameInvalid.grid(column=2, row=2, padx=40, sticky="we")
    else:
        print("Username Invalid!!") 
        lbl_rfBodyUnameInvalid = Label(frm_regBody, text="Invalid! Panjang username 8-45, tanpa spasi", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_rfBodyUnameInvalid.grid(column=2, row=2, padx=40, sticky="we")


    # validating an Email
    regexE = "^[a-z0-9](\.?[a-z0-9A-Z]){0,}@g(oogle)?mail\.com$"
    # akun gmail
    patE = re.compile(regexE)
    # searching regex                 
    matE = re.search(patE, email)

    if matE:
        print("Valid Email")
        valid = valid + 1
        lbl_rfBodyEmailInvalid = Label(frm_regBody, text="Email anda Valid", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_rfBodyEmailInvalid.grid(column=2, row=5, padx=40, sticky="we")  
    else:
        print("Invalid Email")  
        lbl_rfBodyEmailInvalid = Label(frm_regBody, text="Email anda Invalid!!", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_rfBodyEmailInvalid.grid(column=2, row=5, padx=40, sticky="we")   

    # for validating a Password
    regP = "^[^-\s]{8,45}$"
    # tanpa spasi
    # Should be between 8 to 45 characters long.
    # compiling regex
    patP = re.compile(regP)
    # searching regex                 
    matP = re.search(patP, password)

    if matP:
        print("Password is valid.")
        valid = valid+1
        lbl_rfBodyPassInvalid = Label(frm_regBody, text="Password anda Valid", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_rfBodyPassInvalid.grid(column=2, row=7, padx=40, sticky="ew")   
    else:
        print("Password invalid !!")
        lbl_rfBodyPassInvalid = Label(frm_regBody, text="Invalid! Panjang password 8-45, tanpa spasi", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_rfBodyPassInvalid.grid(column=2, row=7, padx=40, sticky="ew")   

    if  password == passwordConfirm :
        print("Password confirmation is valid.")
        valid = valid+1
        lbl_rfBodyPassInvalid = Label(frm_regBody, text="Konfirmasi Password anda Valid", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_rfBodyPassInvalid.grid(column=2, row=9, padx=40, sticky="ew")  
    else:
        print("Password invalid !!")
        lbl_rfBodyPassInvalid = Label(frm_regBody, text="Invalid! Masukkan password yang sama", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_rfBodyPassInvalid.grid(column=2, row=9, padx=40, sticky="ew") 
    
    if valid == 4:
        post = requests.post(urlReg, data = {"username": username , "email": email , "password":  password })
        print(post)
        print(post.text)
        
        if(post.text == "{\"message\":\"Failed! Username is already in use!\"}"):
            print("Username already exists!!") 
            lbl_rfBodyUnameInvalid = Label(frm_regBody, text="Invalid! username already exists", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
            lbl_rfBodyUnameInvalid.grid(column=2, row=2, padx=40, sticky="we")
            pop_regForm.mainloop()
        elif (post.text == "{\"message\":\"Failed! Email is already in use!\"}"):
            print("Email already exists")  
            lbl_rfBodyEmailInvalid = Label(frm_regBody, text="Invalid! username already exists", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
            lbl_rfBodyEmailInvalid.grid(column=2, row=5, padx=40, sticky="we")   
            pop_regForm.mainloop()
        else:
            pop_regForm.destroy()
            loginForm()

    else:
        pop_regForm.mainloop()         


# REGISTRATION FORM
def regForm():
    global pop_regForm
    global ent_rfBodyUname
    global ent_rfBodyPass
    global ent_rfBodyEmail
    global frm_regBody
    global ent_rfBodyPassConfirm
    pop_regForm = Toplevel(homePg)
    pop_regForm.title("ToDoList-Register")
    pop_regForm.rowconfigure(1, weight=1)
    pop_regForm.columnconfigure(0, weight=1)
    pop_regForm.minsize(500,230)
    centered (pop_regForm, 500, 230)


    # registration Form - Header
    lbl_rfHeader = Label(pop_regForm, text="Register", bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

    lbl_rfHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")

    # registration form body
    frm_regBody = Frame(pop_regForm, bg="#FFFFFF")
    lbl_rfBodySpaceN = Label(frm_regBody, bg="#FFFFFF")
    lbl_rfBodySpaceS = Label(frm_regBody, bg="#FFFFFF")
    lbl_rfBodySpaceW = Label(frm_regBody, bg="#FFFFFF")
    lbl_rfBodySpaceE = Label(frm_regBody, bg="#FFFFFF")
    lbl_rfBodyUname = Label(frm_regBody, text="Username", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_rfBodyUname = Entry(frm_regBody, width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000")
    lbl_rfBodyEmail = Label(frm_regBody, text="Email", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_rfBodyEmail = Entry(frm_regBody, width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000")
    lbl_rfBodyEmailNote = Label(frm_regBody, text="*Pastikan email Anda telah terhubung ke Google", bg="#FFFFFF", font=("OpenSans",8), anchor="w")
    lbl_rfBodyPass = Label(frm_regBody, text="Password", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_rfBodyPass = Entry(frm_regBody, width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000", show="*")
    lbl_rfBodyPassConfirm = Label(frm_regBody, text="Konfirmasi Password", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_rfBodyPassConfirm = Entry(frm_regBody, width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000", show="*")    
    btn_rfBodySubmit = Button(frm_regBody, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=regFormSubmit)

    lbl_rfBodySpaceN.grid(column=0, row=0, columnspan=4)
    lbl_rfBodySpaceS.grid(column=0, row=11, columnspan=4)
    lbl_rfBodySpaceW.grid(column=0, row=1, rowspan=10)
    lbl_rfBodySpaceE.grid(column=2, row=1, rowspan=10)
    lbl_rfBodyUname.grid(column=1, row=1, padx=40, sticky="w")
    ent_rfBodyUname.grid(column=2, row=1, padx=40, pady=10)
    lbl_rfBodyEmail.grid(column=1, row=3, padx=40, sticky="w")
    ent_rfBodyEmail.grid(column=2, row=3, padx=40)
    lbl_rfBodyEmailNote.grid(column=2, row=4, padx=40, sticky="w")
    lbl_rfBodyPass.grid(column=1, row=6, padx=40, sticky="w",pady=5)
    ent_rfBodyPass.grid(column=2, row=6, padx=40, pady=10)   
    lbl_rfBodyPassConfirm.grid(column=1, row=8, padx=40, sticky="w",pady=5)
    ent_rfBodyPassConfirm.grid(column=2, row=8, padx=40, pady=10)     
    btn_rfBodySubmit.grid(column=1, row=10, columnspan=2, pady=5)     
    frm_regBody.grid(column=0, row=1, sticky="ensw")
    frm_regBody.rowconfigure([0,11], weight=1)
    frm_regBody.columnconfigure([0,3], weight=1)

# LOGIN FORM SUBMIT
def loginFormSubmit():   
    global username
    global password
    global payload
    global serverAccessToken
    username = ent_loginBodyUname.get()
    password = ent_loginBodyPass.get()

    valid =0

    # for validating a Password
    regP = "^(.|\s)*\S(.|\s)*$"
    # tidak kosong
    # compiling regex
    patP = re.compile(regP)
    # searching regex                 
    matP = re.search(patP, password)

    if matP:
        print("Login Password is valid.")
        valid = valid+1
        lbl_lfBodyPassInvalid = Label(frm_loginBody, text="Ok", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_lfBodyPassInvalid.grid(column=2, row=4, padx=40, sticky="ew")   
    else:
        print("Password invalid !!")
        lbl_lfBodyPassInvalid = Label(frm_loginBody, text="Invalid! Silakan isi password anda", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_lfBodyPassInvalid.grid(column=2, row=4, padx=40, sticky="ew")    

    matU = re.search(patP, username)

    if matU:
        print("Login Username is valid.")
        valid = valid+1
        lbl_lfBodyUnameInvalid = Label(frm_loginBody, text="Ok", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_lfBodyUnameInvalid.grid(column=2, row=2, padx=40, sticky="ew")   
    else:
        print("Login Username invalid !!")
        lbl_rfBodyUnameInvalid = Label(frm_loginBody, text="Invalid! Silakan isi username anda", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_rfBodyUnameInvalid.grid(column=2, row=2, padx=40, sticky="ew")       
           
    if valid == 2:       
        post = requests.post(urlLogin, data={"username": username , "password":  password })
        print(post)
        print(post.text)
        if (post.text == "{\"message\":\"User not found\"}"):
            print("User not found!")
            lbl_rfBodyUnameInvalid = Label(frm_loginBody, text="Invalid! User tidak ditemukan", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
            lbl_rfBodyUnameInvalid.grid(column=2, row=2, padx=40, sticky="ew")
            lbl_rfBodyPassInvalid = Label(frm_loginBody, bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
            lbl_rfBodyPassInvalid.grid(column=2, row=4, padx=40, sticky="ew") 
            ent_loginBodyPass.delete(0,'end')
            pop_loginForm.mainloop()
        elif (post.text == "{\"accessToken\":null,\"message\":\"Password is wrong\"}"):
            print("Wrong password!")
            lbl_rfBodyPassInvalid = Label(frm_loginBody, text="Invalid! Password yang anda masukkan salah", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
            lbl_rfBodyPassInvalid.grid(column=2, row=4, padx=40, sticky="ew") 
            pop_loginForm.mainloop()
        else:
            serverResp = json.loads(post.text)
            print(serverResp)
            serverAccessToken = serverResp['accessToken']
            print(serverAccessToken)            
            pop_loginForm.destroy()
            dashBoard(username,serverAccessToken)
    else : 
        pop_loginForm.mainloop()

    
# LOGIN FORM
def loginForm():
    global pop_loginForm
    global ent_loginBodyUname
    global ent_loginBodyPass
    global frm_loginBody
    pop_loginForm = Toplevel(homePg)
    pop_loginForm.title("ToDoList-Login")
    pop_loginForm.rowconfigure(1, weight=1)
    pop_loginForm.columnconfigure(0, weight=1)
    pop_loginForm.minsize(500,200)
    centered (pop_loginForm, 500, 200)

    # Login Form - Header
    lbl_lfHeader = Label(pop_loginForm, text="Login", bg="#000000", fg="#FFFFFF", font=("OpenSans",15), anchor="center")

    lbl_lfHeader.grid(column=0, row=0, columnspan=2, sticky="ensw")

    # login form body
    frm_loginBody = Frame(pop_loginForm, bg="#FFFFFF")
    lbl_loginBodySpaceN = Label(frm_loginBody, bg="#FFFFFF")
    lbl_loginBodySpaceS = Label(frm_loginBody, bg="#FFFFFF")
    lbl_loginBodySpaceW = Label(frm_loginBody, bg="#FFFFFF")
    lbl_loginBodySpaceE = Label(frm_loginBody, bg="#FFFFFF")
    lbl_loginBodyUname = Label(frm_loginBody, text="Username", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_loginBodyUname = Entry(frm_loginBody, width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000")
    lbl_loginBodyPass = Label(frm_loginBody, text="Password", bg="#FFFFFF", font=("OpenSans",10), anchor="w")
    ent_loginBodyPass = Entry(frm_loginBody, width=40, bg="#FFFFFF", relief=FLAT, highlightthickness=1, highlightbackground = "#000000", show="*")
    btn_loginBodySubmit = Button(frm_loginBody, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=loginFormSubmit)

    lbl_loginBodySpaceN.grid(column=0, row=0, columnspan=4)
    lbl_loginBodySpaceS.grid(column=0, row=6, columnspan=4)
    lbl_loginBodySpaceW.grid(column=0, row=1, rowspan=5)
    lbl_loginBodySpaceE.grid(column=2, row=1, rowspan=5)
    lbl_loginBodyUname.grid(column=1, row=1, padx=40, sticky="w")
    ent_loginBodyUname.grid(column=2, row=1, padx=40, pady=10)
    lbl_loginBodyPass.grid(column=1, row=3, padx=40, sticky="w",pady=5)
    ent_loginBodyPass.grid(column=2, row=3, padx=40, pady=10)   
    btn_loginBodySubmit.grid(column=1, row=5, columnspan=2, pady=10)     
    frm_loginBody.grid(column=0, row=1, sticky="ensw")
    frm_loginBody.rowconfigure([0,6], weight=1)
    frm_loginBody.columnconfigure([0,3], weight=1)    

# HOMEPAGE
homePg = Tk()
homePg.title('ToDoList-Homepage')
homePg.rowconfigure(1, weight=1)
homePg.columnconfigure(0, weight=1)
homePg.minsize(1150,600)
centered (homePg, 1150, 600)

api = "test"
url = 'https://httpbin.org/post'

urlReg = "https://to-do-list-server-pplj.herokuapp.com/register"
urlLogin = "https://to-do-list-server-pplj.herokuapp.com/login"
urlAddActivity = "https://to-do-list-server-pplj.herokuapp.com/addActivity"
urlDeleteActivity = "https://to-do-list-server-pplj.herokuapp.com/deleteactivity"
urlViewActivity = "https://to-do-list-server-pplj.herokuapp.com/viewActivity"
urlAddGroup = "https://to-do-list-server-pplj.herokuapp.com/addGroup"
urlGetGroup = "https://to-do-list-server-pplj.herokuapp.com/getGroup"
urlGetGroupMember = "https://to-do-list-server-pplj.herokuapp.com/getMember"

# photos
photo_lgHeader = PhotoImage(file="header logo.png")
photo_lnBodyTitle = PhotoImage(file="body title line.png")
photo_lgBody = PhotoImage(file="body logo hp.png")
photo_bgBodyLeft = PhotoImage(file="homepage bg left.png")
photo_bgBodyRight = PhotoImage(file="homepage bg right.png")
photo_btnRegister = PhotoImage(file="register button.png")
photo_btnLogin = PhotoImage(file="login button.png")
photo_btnLogout = PhotoImage(file="logout button.png")
photo_btnBack = PhotoImage(file="back button.png")
photo_btnIg = PhotoImage(file="ig logo.png")
photo_btnWA = PhotoImage(file="wa logo.png")
photo_btnMail = PhotoImage(file="mail logo.png")
photo_btnSubmit = PhotoImage (file="submit button.png")
photo_PP = PhotoImage(file="profile picture.png")
photo_1 = PhotoImage(file="icon 1.png")
photo_AAicon = PhotoImage(file="add agenda icon.png")
photo_MAicon = PhotoImage(file="manage agenda icon.png")
photo_btnAA = PhotoImage(file="add agenda button.png")
photo_btnMA = PhotoImage(file="manage agenda button.png")
photo_2 = PhotoImage(file="icon 2.png")
photo_VAicon = PhotoImage(file="view agenda icon.png")
photo_btnVA = PhotoImage(file="view agenda button.png")
photo_3 = PhotoImage(file="icon 3.png")
photo_AGicon = PhotoImage(file="add group icon.png")
photo_btnAG = PhotoImage(file="add group button.png")
photo_DAicon = PhotoImage(file="delete agenda icon.png")
photo_btnDA = PhotoImage(file="delete agenda button.png")
photo_btnDone = PhotoImage(file="done button.png")

# Header
frm_homePgHeader = Frame(homePg, bg="#000000")
lbl_homePgTitle = Label(frm_homePgHeader, bg="#000000", image=photo_lgHeader, borderwidth=0)

lbl_homePgTitle.grid(column=0, row=0)
frm_homePgHeader.grid(column=0, row=0, sticky="ensw")

# Body
# Body - title
frm_homePgBody = Frame(homePg, bg="#FFFFFF", padx=5)
lbl_homePgBodySpaceN = Label(frm_homePgBody, bg="#FFFFFF")
lbl_homePgBodySpaceS = Label(frm_homePgBody, bg="#FFFFFF")
lbl_homePgBodySpaceW = Label(frm_homePgBody, bg="#FFFFFF", image=photo_bgBodyLeft)
lbl_homePgBodySpaceE = Label(frm_homePgBody, bg="#FFFFFF", image=photo_bgBodyRight)
lbl_homePgBodyTitle = Label(frm_homePgBody, bg="#FFFFFF", text="Homepage", font=("OpenSans",15,'bold'))
lbl_homePgBodyTitleLine = Label(frm_homePgBody, bg="#FFFFFF", image=photo_lnBodyTitle,  borderwidth=0)
lbl_homePgBodyGreet = Label(frm_homePgBody, bg="#FFFFFF", text="Halo! Selamat Datang di Aplikasi", font=("OpenSans",20,'bold'), pady=20)
lbl_homePgBodyLogo = Label(frm_homePgBody, bg="#FFFFFF", image=photo_lgBody, borderwidth=0, pady=5)
lbl_homePgBodyHope = Label(frm_homePgBody, bg="#FFFFFF", text="Besar harapan kami aplikasi ini bermanfaat untuk kamu", font=("OpenSans SemiBold",10), pady=5)
lbl_homePgBodyClose = Label(frm_homePgBody, bg="#FFFFFF", text="Salam hangat,\nTim To-do-list", font=("OpenSans",10), pady=5)
btn_register = Button(frm_homePgBody, bg="#FFFFFF", image=photo_btnRegister, borderwidth=0, cursor="hand2", command=regForm)
btn_login = Button(frm_homePgBody, bg="#FFFFFF", image=photo_btnLogin, borderwidth=0, cursor="hand2", command=loginForm)

lbl_homePgBodySpaceN.grid(column=1, row=0, columnspan=2)
lbl_homePgBodySpaceS.grid(column=1, row=8, columnspan=2)
lbl_homePgBodySpaceW.grid(column=0, row=0, rowspan=9, sticky = "s")
lbl_homePgBodySpaceE.grid(column=3, row=0, rowspan=9, sticky = "s")
lbl_homePgBodyTitle.grid(column=1, columnspan=2, row=1)
lbl_homePgBodyTitleLine.grid(column=1, row=2, columnspan=2)
lbl_homePgBodyGreet.grid(column=1, row=3, columnspan=2)
lbl_homePgBodyLogo.grid(column=1, row=4, columnspan=2)
lbl_homePgBodyHope.grid(column=1, row=5, columnspan=2)
lbl_homePgBodyClose.grid(column=1, row=6, columnspan=2)
btn_register.grid(column=1, row=7, pady=15, padx=5)
btn_login.grid(column=2, row=7, pady=15, padx=5)

frm_homePgBody.grid(column=0, row=1, sticky="ensw")
frm_homePgBody.rowconfigure([0,8], weight=1)
frm_homePgBody.columnconfigure([0,3], weight=1)

# Footer
frm_homePgFooter = Frame(homePg, bg="#000000")
lbl_homePgFooterSpaceN = Label(frm_homePgFooter, bg="#000000")
lbl_homePgFooterSpaceS = Label(frm_homePgFooter, bg="#000000")
lbl_homePgFooterSpaceW = Label(frm_homePgFooter, bg="#000000")
lbl_homePgFooterSpaceE = Label(frm_homePgFooter, bg="#000000")
lbl_homePgFooterCP = Label(frm_homePgFooter, bg="#000000", fg="#FFFFFF", text="Hubungi Kami", font=("OpenSans", 8), anchor="e")
lbl_homePgFooterLine = Label(frm_homePgFooter, bg="#FFFFFF", padx=0.1)
btn_homePgFooterIg = Button(frm_homePgFooter, bg="#000000", image=photo_btnIg, cursor="hand2", borderwidth=0 )
btn_homePgFooterWA = Button(frm_homePgFooter, bg="#000000", image=photo_btnWA, cursor="hand2", borderwidth=0)
btn_homePgFooterMail = Button(frm_homePgFooter, bg="#000000", image=photo_btnMail, cursor="hand2",  borderwidth=0)
btn_homePgFooterSK = Button(frm_homePgFooter, bg="#000000", fg="#FFFFFF", text="Syarat Ketentuan", font=("OpenSans", 8), cursor="hand2",  borderwidth=0, anchor="w")
btn_homePgFooterKP = Button(frm_homePgFooter, bg="#000000", fg="#FFFFFF", text="Kebijakan Privasi", font=("OpenSans", 8), cursor="hand2",  borderwidth=0, anchor="w")

lbl_homePgFooterSpaceN.grid(column=0, row=0, columnspan=7, pady=3)
lbl_homePgFooterSpaceS.grid(column=0, row=3, columnspan=7, pady=3)
lbl_homePgFooterSpaceW.grid(column=0, row=1, rowspan=2, padx=10)
lbl_homePgFooterSpaceE.grid(column=6, row=1, rowspan=2, padx=10)
lbl_homePgFooterCP.grid(column=1, row=1, columnspan=3, sticky="ensw")
lbl_homePgFooterLine.grid(column=4, row=1, rowspan=2, sticky="ensw", padx=20)
btn_homePgFooterIg.grid(column=1, row=2, pady=5, padx=5)
btn_homePgFooterWA.grid(column=2, row=2, padx=5)
btn_homePgFooterMail.grid(column=3, row=2, padx=5)
btn_homePgFooterSK.grid(column=5, row=1)
btn_homePgFooterKP.grid(column=5, row=2)
frm_homePgFooter.grid(column=0, row=2, sticky="ensw")
frm_homePgFooter.columnconfigure([0,6], weight=1)

homePg.mainloop()