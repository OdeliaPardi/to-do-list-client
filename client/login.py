from tkinter import *

# LOGIN FORM SUBMIT
def loginFormSubmit():   
    global username
    global password
    global payload
    username = ent_loginBodyUname.get()
    password = ent_loginBodyPass.get()
    payload = "{\n \"username\":\"" + username  +"\",\n \"password\":\"" + password + "\"}"
    print(payload)  
    url = 'https://httpbin.org/post'

    post = requests.post(url,data=payload)
    print(post)
    print(post.text)
    pop_loginForm.destroy()
    dashBoard()

    
# LOGIN FORM
def loginForm():
    global pop_loginForm
    global ent_loginBodyUname
    global ent_loginBodyPass
    pop_loginForm = Tk()
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
    lbl_loginBodySpaceS.grid(column=0, row=5, columnspan=4)
    lbl_loginBodySpaceW.grid(column=0, row=1, rowspan=4)
    lbl_loginBodySpaceE.grid(column=2, row=1, rowspan=4)
    lbl_loginBodyUname.grid(column=1, row=1, padx=40, sticky="w")
    ent_loginBodyUname.grid(column=2, row=1, padx=40, pady=10)
    lbl_loginBodyPass.grid(column=1, row=3, padx=40, sticky="w",pady=5)
    ent_loginBodyPass.grid(column=2, row=3, padx=40, pady=10)   
    btn_loginBodySubmit.grid(column=1, row=4, columnspan=2, pady=10)     
    frm_loginBody.grid(column=0, row=1, sticky="ensw")
    frm_loginBody.rowconfigure([0,5], weight=1)
    frm_loginBody.columnconfigure([0,3], weight=1)    