from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Mini Ap")
root.config(bg="#0A0A0A")
frame = LabelFrame(root, padx=30, pady=120, bg="#171717")
frame.pack(padx=10, pady=10)

first = True
user_info = {}
user_info_list = []
phone_credit = {}
phone_credit_list = []

# card registration
def card_registration():
    global r_root
    r_root = Toplevel()
    r_root.title("Card Registration")
    global r_frame
    r_frame = LabelFrame(r_root, padx=30, pady=120)
    r_frame.pack(padx=10, pady=10)

    registration_label = Label(r_frame, text="Card Registration").grid(row=0, column=0, padx=10, pady=5)
    registration_label = Label(r_frame, text="Continue To Complete The Registration:").grid(row=1, column=0, padx=10, pady=(0, 30))
    global registration_frame
    registration_frame = LabelFrame(r_frame)
    registration_frame.grid(row=2, column=0)
    registration_continue_button = Button(registration_frame, text="Continue", command=signup_name).grid(row=3, column=0, padx=10, pady=10)

# card balance
def card_balance():
    b_root = Toplevel()
    b_root.title("Card Balance")
    b_frame = LabelFrame(b_root, padx=30, pady=120)
    b_frame.pack(padx=10, pady=10)

    balance_label = Label(b_frame, text="Card Balance").grid(row=0, column=0, padx=10, pady=10)
    balance_frame = LabelFrame(b_frame)
    balance_frame.grid(row=1, column=0, padx=10, pady=10)

    def balance_chosen_card_2():
        if len(balance_card_password_entry.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't entered anything")
        else:
            if ( user_info_list[int(balance_card)]["Password"] == str(balance_card_password_entry.get()).strip() ):
                for widget in b_frame.winfo_children():
                    widget.destroy()
                balance_label = Label(b_frame, text="Card Balance").grid(row=0, column=0, padx=10, pady=10)
                balance_frame = LabelFrame(b_frame)
                balance_frame.grid(row=1, column=0, padx=10, pady=10)

                balance_success_label_1 = Label(balance_frame, text="Correct Password!" + "\n" +
                                                                      "Your Card Blance:").grid(row=0, column=0, padx=10, pady=(10, 5))
                balance_succes_label_2 = Label(balance_frame, text=str(user_info_list[int(balance_card)]["Balance"]), font=20)
                balance_succes_label_2.grid(row=1, column=0, padx=10, pady=(0, 10))
            else:
                balance_card_error = messagebox.showerror("Error", "Wrong Password.")

    def balance_chosen_card_1():
        global balance_card
        balance_card = card.get()

        for widget in b_frame.winfo_children():
            widget.destroy()
        balance_label = Label(b_frame, text="Card Balance").grid(row=0, column=0, padx=10, pady=10)
        balance_frame = LabelFrame(b_frame)
        balance_frame.grid(row=1, column=0, padx=10, pady=10)

        balance_card_password_label = Label(balance_frame, text="Please Enter The Password:").grid(row=0, column=0, padx=10, pady=10)
        global balance_card_password_entry
        balance_card_password_entry = Entry(balance_frame, width=20)
        balance_card_password_entry.grid(row=1, column=0, padx=10, pady=(0, 10))

        balance_continue_button = Button(balance_frame, text="Continue", command=balance_chosen_card_2).grid(row=10, column=0, padx=10, pady=(5, 10))

    balance_choose_label = Label(balance_frame, text="Choose Your Card:").grid(row=0, column=0, padx=10, pady=(10, 10))
    card = IntVar()
    for x in range(len(user_info_list)):
        Radiobutton(balance_frame, text=user_info_list[x]["Card Number"], variable=card, value=x).grid(row=x+1, column=0)

    balance_continue_button = Button(balance_frame, text="Continue", command=balance_chosen_card_1).grid(row=10, column=0, padx=10, pady=(8,10))

# charge simcard
def charge_simcard():
    c_root = Toplevel()
    c_root.title("Charge SimCard")
    c_frame = LabelFrame(c_root, padx=30, pady=120)
    c_frame.pack(padx=10, pady=10)

    charge_label = Label(c_frame, text="Charge SimCard").grid(row=0, column=0, padx=10, pady=(10, 30))
    charge_frame = LabelFrame(c_frame)
    charge_frame.grid(row=1, column=0)

    phone_number_label = Label(charge_frame, text="Please Enter The Phone Number:").grid(row=0, column=0, padx=5)
    global phone_number_entry
    phone_number_entry = Entry(charge_frame, width=20)
    phone_number_entry.grid(row=1, column=0, padx=5, pady=(0, 15))

    charge_amount_label = Label(charge_frame, text="Please Enter How Much You Want To Charge:").grid(row=2, column=0, padx=5)
    global charge_amount_entry
    charge_amount_entry = Entry(charge_frame, width=20)
    charge_amount_entry.grid(row=3, column=0, padx=5)

    def charge_phone_2():
        charge_card_number_wanted = charge_card_number_entry.get()
        charge_card_password_wnated = charge_card_password_entry.get()

        if len(charge_card_number_wanted) == 0 or len(charge_card_password_wnated) == 0:
            signup_error = messagebox.showerror("Error", "You haven't completed both of the boxes")
        else:
            y1 = 0
            for x in range(len(user_info_list)):
                if user_info_list[x]["Card Number"] == charge_card_number_wanted:
                    y1 += 1
                    global charge_card_where
                    charge_card_where = int(x)

            if y1 == 0:
                charge_phone_2_error = messagebox.showerror("Error", "This Card Number Is Not In Our System.")
            else:
                if (user_info_list[charge_card_where]["Password"] == charge_card_password_wnated) and (user_info_list[charge_card_where]["Balance"] >= charge_amount_wanted):
                    user_info_list[charge_card_where]["Balance"] -= charge_amount_wanted
                    phone_credit_list[(len(phone_credit_list) - 1)]["Credit"] += charge_amount_wanted

                    for widget in c_frame.winfo_children():
                        widget.destroy()

                    charge_label = Label(c_frame, text="Charge SimCard").grid(row=0, column=0, padx=10, pady=(10, 30))
                    charge_frame = LabelFrame(c_frame)
                    charge_frame.grid(row=1, column=0)

                    charged_simcard_label = Label(charge_frame, text="The SimCard Has Been Successfully Charged!")
                    charged_simcard_label.grid(row=0, column=0, padx=10, pady=10)
                    charged_simcard_amount_label = Label(charge_frame, text="SimCard Credit: " + str(phone_credit_list[(len(phone_credit_list) - 1)]["Credit"]))
                    charged_simcard_amount_label.grid(row=1, column=0, padx=10, pady=(0, 10))
                elif user_info_list[charge_card_where]["Password"] != charge_card_password_wnated:
                    charge_phone_2_error = messagebox.showerror("Error", "Wrong Password.")
                else:
                    charge_phone_2_error = messagebox.showerror("Error", "Not Enough Money In The Card You Entered.")

    def charge_phone_1():
        global phone_number_wanted
        phone_number_wanted = phone_number_entry.get()
        global charge_amount_wanted
        charge_amount_wanted = int(charge_amount_entry.get())

        if len(phone_number_wanted) == 0 or len(charge_amount_entry.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't completed both of the boxes")
        else:
            charge_phone_1_check = [phone_credit_list[x]["Phone Number"] for x in range(len(phone_credit_list))]
            if not (phone_number_wanted in charge_phone_1_check):
                global phone_credit
                phone_credit["Phone Number"] = int(phone_number_wanted)
                phone_credit["Credit"] = 0
                phone_credit_list.append(phone_credit)
                phone_credit = {}

            for widget in c_frame.winfo_children():
                widget.destroy()

            charge_label = Label(c_frame, text="Charge SimCard").grid(row=0, column=0, padx=10, pady=(10, 30))
            charge_frame = LabelFrame(c_frame)
            charge_frame.grid(row=1, column=0)

            charge_card_number_label = Label(charge_frame, text="Please Enter The Card Number:").grid(row=0, column=0, padx=5)
            global charge_card_number_entry
            charge_card_number_entry = Entry(charge_frame, width=20)
            charge_card_number_entry.grid(row=1, column=0, padx=5, pady=(0, 15))

            charge_card_password_label = Label(charge_frame, text="Please Enter The Card Password:").grid(row=2, column=0, padx=5)
            global charge_card_password_entry
            charge_card_password_entry = Entry(charge_frame, width=20)
            charge_card_password_entry.grid(row=3, column=0, padx=5)

            charge_continue_button2 = Button(charge_frame, text="Continue", command=charge_phone_2).grid(row=4, column=0, pady=(15, 10))

    charge_continue_button1 = Button(charge_frame, text="Continue", command=charge_phone_1).grid(row=4, column=0, pady=(15, 10))

# transfer money
def transfer_money():
    t_root = Toplevel()
    t_root.title("Transfer Money")
    t_frame = LabelFrame(t_root, padx=30, pady=120)
    t_frame.pack(padx=10, pady=10)

    transfer_label = Label(t_frame, text="Transfer Money").grid(row=0, column=0, padx=10, pady=10)
    transfer_frame = LabelFrame(t_frame)
    transfer_frame.grid(row=1, column=0, padx=10, pady=10)

    transfer_card_number_label = Label(transfer_frame, text="Please Enter The Card Number" + "\n" + "You Would Like To Send Money From:")
    transfer_card_number_label.grid(row=0, column=0, padx=5, pady=5)
    global transfer_card_number_from_entry
    transfer_card_number_from_entry = Entry(transfer_frame, width=20)
    transfer_card_number_from_entry.grid(row=1, column=0, padx=5, pady=(0, 15))

    transfer_card_password_label = Label(transfer_frame, text="Please Enter The Card Password:").grid(row=2, column=0, padx=5)
    global transfer_card_password_entry
    transfer_card_password_entry = Entry(transfer_frame, width=20)
    transfer_card_password_entry.grid(row=3, column=0, padx=5)

    def transfer_card_3():
        for widget in t_frame.winfo_children():
            widget.destroy()

        transfer_label = Label(t_frame, text="Transfer Money").grid(row=0, column=0, padx=10, pady=10)
        transfer_frame = LabelFrame(t_frame)
        transfer_frame.grid(row=1, column=0, padx=10, pady=10)

        transfer_success_label = Label(transfer_frame, text="The Money Has Been Transferred Successfully!").grid(row=0, column=0, padx=10, pady=(10, 20))

        user_info_list[transfer_card_number_from_where]["Balance"] -= transfer_money_amount_wanted
        user_info_list[transfer_card_number_to_where]["Balance"] += transfer_money_amount_wanted

        transfer_card_from_success = Label(transfer_frame, text="The Balance Of The Card You Send Money From:"
                                                                + "\n" + str(user_info_list[transfer_card_number_from_where]["Balance"]))
        transfer_card_from_success.grid(row=1, column=0, padx=10, pady=(0, 15))

        transfer_card_to_success = Label(transfer_frame, text="The Balance Of The Card You Send Money To:"
                                                              + "\n" + str(user_info_list[transfer_card_number_to_where]["Balance"]))
        transfer_card_to_success.grid(row=2, column=0, padx=10, pady=(0, 15))

    def transfer_card_2():
        global transfer_card_number_to_wanted
        transfer_card_number_to_wanted = transfer_card_number_to_entry.get()
        global transfer_money_amount_wanted
        transfer_money_amount_wanted = int(transfer_money_amount_entry.get())

        if len(transfer_money_amount_entry.get()) == 0 or len(transfer_card_number_to_wanted) == 0:
            signup_error = messagebox.showerror("Error", "You haven't completed both of the boxes")
        else:
            y3 = 0
            for x in range(len(user_info_list)):
                if user_info_list[x]["Card Number"] == transfer_card_number_to_wanted:
                    y3 += 1
                    global transfer_card_number_to_where
                    transfer_card_number_to_where = x

            if y3 == 0:
                transfer_card_2_error = messagebox.showerror("Error", "This Card Number Is Not In The System.")
            elif transfer_card_number_to_wanted == transfer_card_number_from_wanted:
                transfer_card_3_error = messagebox.showerror("Error", "You Have To Enter A Different Card Number From The Last One.")
            elif user_info_list[transfer_card_number_from_where]["Balance"] < transfer_money_amount_wanted:
                transfer_card_2_error = messagebox.showerror("Error", "There Is Not Enough Money In The Card Number You Entered.")
            else:
                for widget in t_frame.winfo_children():
                    widget.destroy()

                transfer_label = Label(t_frame, text="Transfer Money").grid(row=0, column=0, padx=10, pady=10)
                transfer_frame = LabelFrame(t_frame)
                transfer_frame.grid(row=1, column=0, padx=10, pady=10)

                transfer_card_number_name_check_label_1 = Label(transfer_frame, text="The Name Of The Card You Are Sending The Money To:")
                transfer_card_number_name_check_label_1.grid(row=0, column=0, padx=5, pady=5)
                transfer_card_number_name_check_label_2 = Label(transfer_frame, text=str(user_info_list[transfer_card_number_to_where]["Name"]), font=20)
                transfer_card_number_name_check_label_2.grid(row=1, column=0, padx=5, pady=5)

                transfer_continue_button_2 = Button(transfer_frame, text="Continue", command=transfer_card_3).grid(row=4, column=0, pady=(15, 10))
    def transfer_card_1():
        global transfer_card_number_from_wanted
        transfer_card_number_from_wanted = transfer_card_number_from_entry.get()
        global transfer_card_password_from_wanted
        transfer_card_password_from_wanted = transfer_card_password_entry.get()

        if len(transfer_card_number_from_wanted) == 0 or len(transfer_card_password_from_wanted) == 0:
            signup_error = messagebox.showerror("Error", "You haven't completed both of the boxes")
        else:
            y2 = 0
            for x in range(len(user_info_list)):
                if user_info_list[x]["Card Number"] == transfer_card_number_from_wanted:
                    y2 += 1
                    global transfer_card_number_from_where
                    transfer_card_number_from_where = x

            if y2 == 0:
                transfer_card_1_error = messagebox.showerror("Error", "This Card Number Is Not In Our System")
            elif user_info_list[transfer_card_number_from_where]["Password"] != transfer_card_password_from_wanted:
                transfer_card_1_error = messagebox.showerror("Error", "Wrong Password")
            else:
                for widget in t_frame.winfo_children():
                    widget.destroy()

                transfer_label = Label(t_frame, text="Transfer Money").grid(row=0, column=0, padx=10, pady=10)
                transfer_frame = LabelFrame(t_frame)
                transfer_frame.grid(row=1, column=0, padx=10, pady=10)

                transfer_card_number_label = Label(transfer_frame, text="Please Enter The Card Number" + "\n" + "You Would Like To Send Money To:")
                transfer_card_number_label.grid(row=0, column=0, padx=5, pady=5)
                global transfer_card_number_to_entry
                transfer_card_number_to_entry = Entry(transfer_frame, width=20)
                transfer_card_number_to_entry.grid(row=1, column=0, padx=5, pady=(0, 15))

                transfer_money_amount_label = Label(transfer_frame, text="Please Enter The Amount You Would Like To Transfer:")
                transfer_money_amount_label.grid(row=2, column=0, padx=5)
                global transfer_money_amount_entry
                transfer_money_amount_entry = Entry(transfer_frame, width=20)
                transfer_money_amount_entry.grid(row=3, column=0, padx=5)

                transfer_continue_button_1 = Button(transfer_frame, text="Continue", command=transfer_card_2).grid(row=4, column=0, pady=(15, 10))

    transfer_continue_button1 = Button(transfer_frame, text="Continue", command=transfer_card_1).grid(row=4, column=0, pady=(15, 10))

# main menu
def main_manu():
    global first
    if first:
        first = False
        for widget in frame.winfo_children():
            widget.destroy()

    sth_label = Label(frame, text="Hi! What Would You Like To Do Today?").grid(row=0, column=0, pady=(10, 30))

    sth_frame = LabelFrame(frame)
    sth_frame.grid(row=1, column=0)

    card_balance_button = Button(sth_frame, text="Card Balance", width=20, command=card_balance).grid(row=0, column=0, padx=10, pady=10)
    card_registration_button = Button(sth_frame, text="Card Registration", width=20, command=card_registration).grid(row=1, column=0, padx=10, pady=10)
    transfer_money_button = Button(sth_frame, text="Transfer Money", width=20, command=transfer_money).grid(row=2, column=0, padx=10, pady=10)
    charge_simcard_button = Button(sth_frame, text="Charge Simcard", width=20, command=charge_simcard).grid(row=3, column=0, padx=10, pady=10)

# sign up OR card registration
def signup_to_mainmenu():
    if first:
        if len(password_entry_1.get()) == 0 or len(password_entry_2.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't completed both of the boxes")
        else:
            if ( str(password_entry_2.get()).strip() == str(password_entry_1.get()).strip() ):
                global user_info
                global phone_credit
                user_info["Password"] = str(password_entry_1.get()).strip()
                user_info["Balance"] = 100000
                phone_credit["Credit"] = 0
                user_info_list.append(user_info)
                phone_credit_list.append(phone_credit)
                user_info = {}
                phone_credit = {}

                for widget in frame.winfo_children():
                    widget.destroy()

                registration_label = Label(frame, text="Card Registration").grid(row=0, column=0, padx=10, pady=5)
                registration_frame_2 = LabelFrame(frame)
                registration_frame_2.grid(row=2, column=0)
                continue_registration_label = Label(registration_frame_2, text="You Have Successfully Signed Up!").grid(row=1, column=0, padx=10, pady=(10, 5))
                mainmenu_button = Button(registration_frame_2, text="Main Menu",command=main_manu).grid(row=5, column=0, padx=10, pady=10)
            else:
                signup_message_error = messagebox.showerror("Error", "Please Enter The Same Password In The Two Boxes.")
    else:
        if len(r_password_entry_1.get()) == 0 or len(r_password_entry_2.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't completed both of the boxes")
        else:
            if ( str(r_password_entry_1.get()).strip() == str(r_password_entry_2.get()).strip() ):
                user_info["Password"] = str(r_password_entry_1.get()).strip()
                user_info["Balance"] = 100000
                phone_credit["Credit"] = 0
                user_info_list.append(user_info)
                phone_credit_list.append(phone_credit)
                user_info = {}
                phone_credit = {}

                for widget in r_frame.winfo_children():
                    widget.destroy()

                registration_label = Label(r_frame, text="Card Registration").grid(row=0, column=0, padx=10, pady=5)
                registration_frame_2 = LabelFrame(r_frame)
                registration_frame_2.grid(row=1, column=0)

                continue_registration_label = Label(registration_frame_2, text="The New Card Has Been" + "\n"
                                                                               + "Successfully Registered!")
                continue_registration_label.grid(row=0, column=0, padx=10, pady=(10, 10))
            else:
                r_signup_message_error = messagebox.showerror("Error", "Please Enter The Same Password In The Two Boxes.")

def signup_password():
    if first:
        if len(phone_entry.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't entered anything")
        else:
            phone_credit["Phone Number"] = phone_entry.get()
            for widget in frame.winfo_children():
                widget.destroy()

            welcome_label = Label(frame, text="Welcome To Mini Ap!", font=50).grid(row=0, column=0, padx=10, pady=5)
            signup_label = Label(frame, text="Please Sign Up For An Account.").grid(row=1, column=0, padx=10, pady=(0, 40))
            signup_frame_2 = LabelFrame(frame)
            signup_frame_2.grid(row=2, column=0)

            password_label_1 = Label(signup_frame_2, text="Please Enter Your Password:").grid(row=1, column=0, padx=10)
            global password_entry_1
            password_entry_1 = Entry(signup_frame_2, width=25)
            password_entry_1.grid(row=2, column=0)
            password_label_2 = Label(signup_frame_2, text="Repeat The Password:").grid(row=3, column=0, padx=10)
            global password_entry_2
            password_entry_2 = Entry(signup_frame_2, width=25)
            password_entry_2.grid(row=4, column=0)
            continue_continue = Button(signup_frame_2, text="Continue", command=signup_to_mainmenu).grid(row=5, column=0,padx=10, pady=10)
    else:
        if len(r_phone_entry.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't entered anything")
        else:
            signup_phonenumber_check = [phone_credit_list[x]["Phone Number"] for x in range(len(phone_credit_list))]
            if (r_phone_entry.get() in signup_phonenumber_check):
                signup_phonenumber_error = messagebox.showerror("Error", "This Phone Number Already Exists")
            else:
                phone_credit["Phone Number"] = r_phone_entry.get()
                for widget in r_frame.winfo_children():
                    widget.destroy()

                registration_label = Label(r_frame, text="Card Registration").grid(row=0, column=0, padx=10, pady=5)
                continue_registration_label = Label(r_frame, text="Continue To Complete The Registration:").grid(row=1, column=0, padx=10, pady=(0, 40))
                registration_frame_2 = LabelFrame(r_frame)
                registration_frame_2.grid(row=2, column=0)

                r_password_label_1 = Label(registration_frame_2, text="Please Enter Your Password:").grid(row=1, column=0, padx=10)
                global r_password_entry_1
                r_password_entry_1 = Entry(registration_frame_2, width=25)
                r_password_entry_1.grid(row=2, column=0)
                r_password_label_2 = Label(registration_frame_2, text="Repeat The Password:").grid(row=3, column=0, padx=10)
                global r_password_entry_2
                r_password_entry_2 = Entry(registration_frame_2, width=25)
                r_password_entry_2.grid(row=4, column=0)
                r_continue_button = Button(registration_frame_2, text="Continue", command=signup_to_mainmenu).grid(row=5, column=0, padx=10, pady=10)

def signup_phonenumber():
    if first:
        if len(card_entry.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't entered anything")
        else:
            user_info["Card Number"] = card_entry.get()
            phone_label = Label(signup_frame, text="Please Enter Your Phone Number:").grid(row=1, column=0, padx=10)
            global phone_entry
            phone_entry = Entry(signup_frame, width=25)
            phone_entry.grid(row=2, column=0)
            continue_button = Button(signup_frame, text="Continue", command=signup_password).grid(row=3, column=0, padx=10, pady=10)
    else:
        if len(r_card_entry.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't entered anything")
        else:
            signup_cardnumber_check = [user_info_list[x]["Card Number"] for x in range(len(user_info_list))]
            if (r_card_entry.get() in signup_cardnumber_check):
                signup_cardnumber_error = messagebox.showerror("Error", "This Card Number Already Exists.")
            else:
                user_info["Card Number"] = r_card_entry.get()
                r_phone_label = Label(registration_frame, text="Please Enter Your Phone Number:").grid(row=1, column=0, padx=10)
                global r_phone_entry
                r_phone_entry = Entry(registration_frame, width=25)
                r_phone_entry.grid(row=2, column=0)
                r_continue_button = Button(registration_frame, text="Continue", command=signup_password).grid(row=3, column=0, padx=10, pady=10)

def signup_cardnumber():
    if first:
        if len(name_entry.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't entered anything")
        else:
            user_info["Name"] = str(name_entry.get()).lower()
            card_label = Label(signup_frame, text="Please Enter Your Card Number:").grid(row=1, column=0, padx=10)
            global card_entry
            card_entry = Entry(signup_frame, width=25)
            card_entry.grid(row=2, column=0)
            continue_button = Button(signup_frame, text="Continue", command=signup_phonenumber).grid(row=3, column=0, padx=10, pady=10)
    else:
        if len(r_name_entry.get()) == 0:
            signup_error = messagebox.showerror("Error", "You haven't entered anything")
        else:
            user_info["Name"] = str(r_name_entry.get()).lower()
            r_card_label = Label(registration_frame, text="Please Enter The Card Number:").grid(row=1, column=0, padx=10)
            global r_card_entry
            r_card_entry = Entry(registration_frame, width=25)
            r_card_entry.grid(row=2, column=0)
            r_continue_button = Button(registration_frame, text="Continue", command=signup_phonenumber).grid(row=3, column=0, padx=10, pady=10)

def signup_name():
    if first:
        name_label = Label(signup_frame, text="Please Enter Your Full Name:").grid(row=1, column=0, padx=10)
        global name_entry
        name_entry = Entry(signup_frame, width=25)
        name_entry.grid(row=2, column=0, padx=10)
        continue_button = Button(signup_frame,text="Continue", command=signup_cardnumber).grid(row=3, column=0, padx=10, pady=10)
    else:
        r_name_label = Label(registration_frame, text="Please Enter The Full Name:").grid(row=1, column=0, padx=10)
        global r_name_entry
        r_name_entry = Entry(registration_frame, width=25)
        r_name_entry.grid(row=2, column=0, padx=10)
        r_continue_button = Button(registration_frame, text="Continue", command=signup_cardnumber).grid(row=3, column=0, padx=10, pady=10)

if first:
    welcome_label = Label(frame, text="Welcome To Mini Ap!", font=50, bg="#171717", fg="#E2E2E2").grid(row=0, column=0, padx=10, pady=5)
    signup_label = Label(frame, text="Please Sign Up For An Account.", bg="#171717", fg="#E2E2E2").grid(row=1, column=0, padx=10, pady=(0, 40))
    signup_frame = LabelFrame(frame, bg="#171717")
    signup_frame.grid(row=2, column=0)
    start_button = Button(signup_frame, text="Start", command=signup_name, width=7, bg="#BC87FC", fg="#0A0A0A").grid(row=3, column=0, padx=10, pady=10)

# end stuff
button_quit = Button(root, text="Exit Program", command=root.quit, bg="#171717", fg="#E2E2E2")
button_quit.pack(pady=(0, 10))

root.mainloop()