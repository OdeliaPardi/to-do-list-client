import tkinter as tk

# def response(regform):
#     lbl_regF_okresp = tk.Label(regform, text="registered!")
#     # lbl_regF_wspace_regresp = tk.Label(regform)
#     # lbl_regF_espace_regresp = tk.Label(regform)

#     lbl_regF_okresp.pack()
#     # lbl_regF_okresp.grid(column=0, row=5, columnspan=2)
#     # lbl_regF_wspace_regresp.grid(column=0, row=5, padx=35)
#     # lbl_regF_espace_regresp.grid(column=3, row=5, padx=35)
#     return

def reg_form():
    regform = tk.Tk()
    regform.title("To Do List - Registration Form")

    regform.minsize(400, 400)

    frm_regform = tk.Frame(regform)

    # lbl_regF_nspace = tk.Label(frm_regform)
    # lbl_regF_sspace = tk.Label(frm_regform)
    # lbl_regF_wspace_ent = tk.Label(frm_regform)
    # lbl_regF_espace_ent = tk.Label(frm_regform)
    # lbl_regF_wspace_btn = tk.Label(frm_regform)
    # lbl_regF_espace_btn = tk.Label(frm_regform)

    # lbl_regF_nspace.grid(column=0, row = 0, columnspan=3, pady = 30)
    # lbl_regF_sspace.grid(column=0, row=7, columnspan=3, pady=30)
    # lbl_regF_wspace_ent.grid(column=0, row=1, rowspan=4, padx = 30)
    # lbl_regF_espace_ent.grid(column=3, row=1, rowspan=4, padx=30)
    # lbl_regF_wspace_btn.grid(column=0, row=5, padx=35)
    # lbl_regF_espace_btn.grid(column=3, row=1, padx=35)
    

    # Registration Form Title
    lbl_regF_title = tk.Label(frm_regform, text="Register", font=("Times New Roman", 20))

    lbl_regF_title.grid(column = 0, row = 0, columnspan=2, sticky="ew", pady=10)

    # Registration Form Label
    lbl_regF_uname = tk.Label(frm_regform, text="Username", font=("Times New Roman",10))
    lbl_regF_email = tk.Label(frm_regform, text="Email", font=("Times New Roman",10))
    lbl_regF_pass = tk.Label(frm_regform, text="Password", font=("Times New Roman",10))

    lbl_regF_uname.grid(column=0, row=1, sticky="w")
    lbl_regF_email.grid(column=0, row=2, sticky="w")
    lbl_regF_pass.grid(column=0, row=3, sticky="w")

    # Registration Form Entry
    ent_regF_uname = tk.Entry(frm_regform)
    ent_regF_email = tk.Entry(frm_regform)
    ent_regF_pass = tk.Entry(frm_regform)

    ent_regF_uname.grid(column=1, row=1, sticky="ew")
    ent_regF_email.grid(column=1, row=2, sticky="ew")
    ent_regF_pass.grid(column=1, row=3, sticky="ew")

    # Registration Form Button
    btn_regF_ok = tk.Button(frm_regform, text="Register", padx=20)

    btn_regF_ok.grid(column=0, row=4, columnspan=2, pady=10)

    frm_regform.pack(expand=True)
    
    regform.mainloop()

def login_form():
    loginform = tk.Tk()
    loginform.title("To Do List - Login Form")

    loginform.minsize(400,400)

    frm_loginform = tk.Frame(loginform)

    # lbl_logF_nspace = tk.Label(frm_loginform)
    # lbl_logF_sspace = tk.Label(frm_loginform)
    # lbl_logF_wspace_ent = tk.Label(frm_loginform)
    # lbl_logF_espace_ent = tk.Label(frm_loginform)
    # lbl_logF_wspace_btn = tk.Label(frm_loginform)
    # lbl_logF_espace_btn = tk.Label(frm_loginform)

    # lbl_logF_nspace.grid(column=0, row = 0, columnspan=3, pady = 30)
    # lbl_logF_sspace.grid(column=0, row=5, columnspan=3, pady=30)
    # lbl_logF_wspace_ent.grid(column=0, row=1, rowspan=3, padx = 30)
    # lbl_logF_espace_ent.grid(column=3, row=1, rowspan=3, padx=30)
    # lbl_logF_wspace_btn.grid(column=0, row=4, padx=35)
    # lbl_logF_espace_btn.grid(column=3, row=1, padx=35)
    

    # Login Form Title
    lbl_logF_title = tk.Label(frm_loginform, text="Login", font=("Times New Roman", 20))

    lbl_logF_title.grid(column = 0, row = 0, columnspan=2, sticky="ew", pady=10)

    # Login Form Label
    lbl_logF_uname = tk.Label(frm_loginform, text="Username", font=("Times New Roman",10))
    lbl_logF_pass = tk.Label(frm_loginform, text="Password", font=("Times New Roman",10))

    lbl_logF_uname.grid(column=0, row=1, sticky="w")
    lbl_logF_pass.grid(column=0, row=2, sticky="w")

    # Login Form Entry
    ent_logF_uname = tk.Entry(frm_loginform)
    ent_logF_pass = tk.Entry(frm_loginform)

    ent_logF_uname.grid(column=1, row=1, sticky="ew")
    ent_logF_pass.grid(column=1, row=2, sticky="ew")

    # Login Form Button
    btn_logF_ok = tk.Button(frm_loginform, text="Login", padx=20)

    btn_logF_ok.grid(column=0, row=3, columnspan=2, pady=10)

    frm_loginform.pack(expand=True)
    
    loginform.mainloop()    


# homepage
homepage = tk.Tk()
# homepage title
homepage.title("To Do List - Homepage")
# homepage min size
homepage.minsize(400, 400)
# homepage color
# homepage.configure(bg="blue")

#homepage frame
frm_homepg = tk.Frame(homepage)

# lbl_homepg_nspace = tk.Label(frm_homepg)
# lbl_homepg_sspace = tk.Label(frm_homepg)
# lbl_homepg_wspace = tk.Label(frm_homepg)
# lbl_homepg_espace = tk.Label(frm_homepg)

# lbl_homepg_nspace.grid(column = 0, row = 0, columnspan=3, pady = 30)
# lbl_homepg_sspace.grid(column=0, row=4, columnspan=3, pady=30)
# lbl_homepg_wspace.grid(column = 0, row = 2, rowspan=2, padx = 30)
# lbl_homepg_espace.grid(column=2, row=2, rowspan=2, padx=30)

# Homepage Title
lbl_title = tk.Label(frm_homepg, text="To do list", font=("Times New Roman", 20))

lbl_title.grid(column = 0, row = 0, columnspan=3, sticky="ew", pady=10)

# Register and Login Buttons
btn_register = tk.Button (frm_homepg, text = "Register", font=("Times New Roman",10), command=reg_form)
btn_login = tk.Button (frm_homepg, text="Login", font=("Times New Roman",10), command=login_form)

btn_register.grid(row=1, column=0, sticky="ew", padx = 50, pady = 5)
btn_login.grid(row=2,column=0, sticky="ew", padx = 50, pady = 5)

frm_homepg.pack(expand=True)

homepage.mainloop()






