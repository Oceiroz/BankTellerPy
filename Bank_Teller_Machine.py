import random
import os

def main():
    global account_path
    account_path = "Accounts"
    global account_id
    if menu() == 1:
        account_id = sign_in()
    elif menu() == 2:
        account_id = create_account()

    with open(f"{account_path}\\{account_id}.txt") as f:
        lines = [line.rstrip() for line in f]
        global f_name
        f_name = lines[0]
        global l_name
        l_name = lines[1]
        global money
        money = lines[2]
        global password
        password = lines[3]
        global overdraft_bool
        overdraft_bool = lines[4]
        global overdraft_amount
        overdraft_amount = lines[5]

        account_info(f_name, l_name, money, password, overdraft_bool, overdraft_amount)   

  
def get_input(input_message, input_type):
    while(True):
        raw_input = input(f"{input_message}\n")
        try:
            user_input = input_type(raw_input)
            break
        except ValueError:
            print(f"Not a valid input.\n")
    return user_input

def get_choice(input_message, choices):
    while(True):
        
        for x, choice in enumerate(choices):
            print(x+1, choices[x])
            
        raw_input = input(f"\n{input_message}\n")
        try:
            user_input = int(raw_input)
            if user_input > len(choices) or user_input < 1:
                raise ValueError
            break
        except ValueError:
            print(f"Not a valid option. Pick a number from 1 to {len(choices)}.\n")
    return user_input


def get_accounts():
    account_list = os.listdir(account_path)
    account_list_clean = []
    for x in (account_list):
        new_account_name = x.strip(".txt")
        account_list_clean.append(new_account_name)    
    
    return account_list_clean
        
def menu():
    options = ["Sign-in", "Create Account"]
    sign_create = get_choice("What would you like to do:", options)
    return sign_create

def create_account():
    #account number   
    account_number = random.randint(0,99999999)
    account_id = "%08d" % account_number
    # f_name
    f_name = get_input("What is your first name?", str)
    # l_name
    l_name = get_input("What is your last name?", str)
    # money
    money = get_input("How much money do you have?", float)
    # pin
    while(True):
        password = get_input("please input a 4 digit pin", int)
        if len(str(password)) == 4:
            break
        else:
            print("Pin is not 4 digits, please try again\n")
            
    while(True):
        pin_confirm = get_input("please re-enter new pin", int)
        if pin_confirm == password:
            print("Your pin has been set.\n")
            print(f"your account id is: {account_id}. Do not forget this.\n")
            break
        else:
            print("New pin does not match initial pin. Please try again.\n")
    
    #overdraft placeholder
    overdraft_bool = "False"
    overdraft_amount = 0
    
    #account saving
    account_file_content = [f"{f_name}\n", f"{l_name}\n", f"{money}\n", f"{password}\n", f"{overdraft_bool}\n", f"{overdraft_amount}\n"]
    account_file_create = open(f"{account_path}\\{account_id}.txt", "w")
    for x, file in enumerate(account_file_content):
        account_file_create.writelines(f"{account_file_content[x]}")
        print (account_file_content[x])
    account_file_create.close() 
    return account_id
    
def sign_in():
    #account number input
    account_list = get_accounts()
    account_found = False
    account_id = get_input("Please type in account 8-digit number:", int)
    account_id = f"{account_id:08d}"
    for x, account in enumerate(account_list):
        if account_id == account_list[x]:
            account_found = True
            break
    #reenter id when account not found            
    if account_found == False:
        options = ["Yes", "No"]
        re_find = get_choice("You may have typed in your number wrong, would you like to try again:", options)
        if re_find == 1:
            sign_in()
        elif re_find == 2:
            print("Please make an account")
            menu()
      
    #password input
    with open(f"{account_path}\\{account_id}.txt") as f:
        lines = [line.rstrip() for line in f]
        password = lines[3]
    while(True):
        pin_input = get_input("Please input your 4-digit pin", int)
        if pin_input == int(password):
            break
        elif pin_input != int(password):
            print("You typed in the pin wrong. Please try again\n")
    
    return account_id    


def account_info(f_name, l_name, money, password, overdraft_bool, overdraft_amount):
    print(f"\n{account_id}",f"\n{f_name}{l_name}\n")
    #account options
    options = ["Balance", "Deposit", "Withdrawal", "Overdraft", "Help", "Sign-out"]
    account_option = get_choice("Where would you like to go:", options)
    #balance
    if account_option == 1:
        account_balance(money)
    #deposit
    elif account_option == 2:
        deposit_money(money)
    #withdrawal
    elif account_option == 3:
        withdraw_money(money, overdraft_bool, overdraft_amount)
    #overdraft
    elif account_option == 4:
        overdraft_apply(overdraft_bool, overdraft_amount)
    #help
    elif account_option == 5:
        help_menu()
    #sign out
    elif account_option == 6:  
        sign_out(f_name, l_name, money, password, overdraft_bool, overdraft_amount)
       
def account_balance(money):
    #balance
    while(True):
        print("Your current balance is:\n")
        print(f"{money}")
        options = ["Yes", "No"]
        get_out = get_choice("Are you finished in this section?", options)
        if get_out == 1:
            break
    account_info(f_name, l_name, money, password, overdraft_bool, overdraft_amount)
    
           
def deposit_money(money):
    while(True):
        amount = get_input("How much would you like to add", float)
        #add money
        money = float(money) + amount
        print("Your total is now:\n", f"{money}")
        options = ["Yes", "No"]
        get_out = get_choice("Are you finished in this section?", options)
        if get_out == 1:
            break
    account_info(f_name, l_name, money, password, overdraft_bool, overdraft_amount)
      
def withdraw_money(money, overdraft_bool, overdraft_amount):
    #remove money
    while(True):
        remove_amount = get_input("How much money would you like to withdraw", float)
        remove_money = float(money) - remove_amount
        if remove_money < 0 and overdraft_bool == "False":
            print("Money cannot be removed as you do not have enough in your total and you do not have an overdraft\n")
        elif remove_money < 0 and overdraft_bool == "True":
            overdraft_check = float(overdraft_amount) + remove_money
            if overdraft_check < 0:
                print("You do not have enough in your overdraft to withdraw this money. Please try again\n")
            else:
                print("Money was succesfully withdrawn. Please bare in mind you are using your overdraft\n")
                money = remove_money
                print("Your total is now:", f"{money}")
            options = ["Yes", "No"]
            get_out = get_choice("Are you finished in this section?", options)
            if get_out == 1:
                break
        elif remove_money >= 0:
            print("Money was succesfully withdrawn\n")
            money = remove_money
            print("Your total is now:", f"{money}")
            options = ["Yes", "No"]
            get_out = get_choice("Are you finished in this section?", options)
            if get_out == 1:
                break
    account_info(f_name, l_name, money, password, overdraft_bool, overdraft_amount)
                 
def overdraft_apply(overdraft_bool, overdraft_amount):
    while(True):    
        #overdraft check
        if overdraft_bool == "True":
            #overdraft options
            options_change = ["View", "Change", "Remove"]
            change_overdraft = get_choice("What would you like to do with your overdraft", options_change)
            if change_overdraft == 1:
                print("Your current overdraft is:", f"{overdraft_amount}")
                
            elif change_overdraft == 2:
                overdraft_amount = get_input("What would you like your overdraft amount to be:", float)
                
            elif change_overdraft == 3:
                overdraft_bool = "False"
                overdraft_amount = 0
                print("You no longer have an overdraft")
            options = ["Yes", "No"]
            get_out = get_choice("Are you finished in this section?", options)
            if get_out == 1:
                 break
        
        elif overdraft_bool == "False":
            options = ["Yes", "No"]
            new_overdraft = get_choice("Would you like to make an overdraft:", options)
            #overdraft create
            if new_overdraft == 1:
                overdraft_amount = get_input("How much overdraft would you like:", float)
                overdraft_bool = "True"
            elif new_overdraft == 2:
                print("That is fine, you can always come back later if you change your mind.")
            options = ["Yes", "No"]
            get_out = get_choice("Are you finished in this section?", options)
            if get_out == 1:
                break
    account_info(f_name, l_name, money, password, overdraft_bool, overdraft_amount)
                
def help_menu():
    while(True):
        balance = "\nThe balance is how much money you have.\nIf the number is negative, it will be because you have an overdraft\n"
        deposit = "\nThe deposit is how much money you are looking to add to the account.\n"
        withdraw = "\nThe withdraw is how much money you are taking out of the account.\nIf you have an overdraft you can take out your total plus the amount your overdraft is.\n"
        overdraft = "\nThe overdraft is how much money you will have available to you after passing 0 before your account goes bankrupt.\n"
        options = ["balance", "deposit", "withdraw", "overdraft"]
        get_help = get_choice("What do you need help with:", options)
        if get_help == 1:
            print(f"{balance}")
        elif get_help == 2:
            print(deposit)
        elif get_help == 3:
            print(withdraw)
        elif get_help == 4:
            print(overdraft)

        options = ["Yes", "No"]
        get_out = get_choice("Are you finished in this section?", options)
        if get_out == 1:
            break
    account_info(f_name, l_name, money, password, overdraft_bool, overdraft_amount)
    
def finish():
    options = ["Yes", "No"]
    get_out = get_choice("Are you finished in this section?", options)
    if get_out == 1:
        account_info(f_name, l_name, money, password, overdraft_bool, overdraft_amount)
    elif get_out == 2:
        print("okay")
    return         
        
    
def sign_out(f_name, l_name, money, password, overdraft_bool, overdraft_amount):
    options = ["Yes", "No"]
    get_out = get_choice("Are you sure you would like to sign out:", options)
    if get_out == 1:
        account_file_content = [f"{f_name}\n", f"{l_name}\n", f"{money}\n", f"{password}\n", f"{overdraft_bool}\n", f"{overdraft_amount}\n"]
        account_file_create = open(f"{account_path}\\{account_id}.txt", "w")
        for x, file in enumerate(account_file_content):
            account_file_create.writelines(f"{account_file_content[x]}")
        account_file_create.close()
    elif get_out == 2:
        account_info()
    
main()