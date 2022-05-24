from tkinter import *
from login import *


def centered(window, width, height):
    # Gets both half the screen width/height and window width/height
    positionRight = int(window.winfo_screenwidth()/2 - width/2)
    positionDown = int(window.winfo_screenheight()/2 - height/2)
    
    # Positions the window in the center of the page.
    window.geometry("+{}+{}".format(positionRight, positionDown))



# REGISTRATION FORM SUBMIT
def regFormSubmit():
    global username
    global password
    global email
    global valid
    global payload
    global lbl_rfBodyUnameInvalid
    global lbl_rfBodyEmailInvalid
    global lbl_rfBodyPassInvalid
    username = ent_rfBodyUname.get()
    password = ent_rfBodyPass.get()
    email = ent_rfBodyEmail.get()
    valid=0

    # validating username
    regexU = "^[^-\s]{8,45}$"
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
    regexE = r'^[A-Za-z0-9!@#$%^&*]@g(oogle)?mail\.com$'

    if(re.fullmatch(regexE, email)):
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
    pat = re.compile(regP)
    # searching regex                 
    mat = re.search(pat, password)

    if mat:
        print("Password is valid.")
        valid = valid+1
        lbl_rfBodyPassInvalid = Label(frm_regBody, text="Password anda Valid", bg="#FFFFFF", fg="green", font=("OpenSans",8), anchor="w")
        lbl_rfBodyPassInvalid.grid(column=2, row=7, padx=40, sticky="ew")   
    else:
        print("Password invalid !!")
        lbl_rfBodyPassInvalid = Label(frm_regBody, text="Invalid! Panjang password 8-45, tanpa spasi", bg="#FFFFFF", fg="red", font=("OpenSans",8), anchor="w")
        lbl_rfBodyPassInvalid.grid(column=2, row=7, padx=40, sticky="ew")   
    
    if valid == 3:
        payload = "{\n \"username\":\"" + username  +"\",\n \"email\": \""+ email +"\",\n \"password\":\"" + password + "\"}"
        print(payload)  
        url = 'https://httpbin.org/post'

        post = requests.post(url,data=payload)
        print(post)
        print(post.text)

        # cek respon API dulu

        pop_regForm.destroy()
        loginForm()
    else:
        pop_regForm.mainloop()         


photo_btnSubmit = PhotoImage (file="submit button.png")

# REGISTRATION FORM
def regForm():
    global pop_regForm
    global ent_rfBodyUname
    global ent_rfBodyPass
    global ent_rfBodyEmail
    global frm_regBody
    pop_regForm = Tk()
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
    btn_rfBodySubmit = Button(frm_regBody, bg="#FFFFFF", image=photo_btnSubmit, cursor="hand2",  borderwidth=0, command=regFormSubmit)

    lbl_rfBodySpaceN.grid(column=0, row=0, columnspan=4)
    lbl_rfBodySpaceS.grid(column=0, row=9, columnspan=4)
    lbl_rfBodySpaceW.grid(column=0, row=1, rowspan=8)
    lbl_rfBodySpaceE.grid(column=2, row=1, rowspan=8)
    lbl_rfBodyUname.grid(column=1, row=1, padx=40, sticky="w")
    ent_rfBodyUname.grid(column=2, row=1, padx=40, pady=10)
    lbl_rfBodyEmail.grid(column=1, row=3, padx=40, sticky="w")
    ent_rfBodyEmail.grid(column=2, row=3, padx=40)
    lbl_rfBodyEmailNote.grid(column=2, row=4, padx=40, sticky="w")
    lbl_rfBodyPass.grid(column=1, row=6, padx=40, sticky="w",pady=5)
    ent_rfBodyPass.grid(column=2, row=6, padx=40, pady=10)   
    btn_rfBodySubmit.grid(column=1, row=8, columnspan=2, pady=5)     
    frm_regBody.grid(column=0, row=1, sticky="ensw")
    frm_regBody.rowconfigure([0,9], weight=1)
    frm_regBody.columnconfigure([0,3], weight=1)