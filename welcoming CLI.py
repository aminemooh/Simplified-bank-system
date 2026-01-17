from Bank system import bankaccount

def welcoming_software(B1):
        name, id_num, user_id = None, None ,None
        while True:
            iteration = int(input('''
            ================================================================================================================
                                                 Welcome to The Banking System                                                            
            ================================================================================================================
            What would you like us to help you with today?
            Chose from the follwoing services : 
            1) Creat an account.
            2) Check Balance.
            3) Deposit money.
            4) Widthdraw money.
            5) Close an account.
            6) log out of current Account.
            7) Quit software.
            Enter the operation you are looking to : '''))
            if iteration == 7:
                print("Thank you for using our system, Goodbye!")
                break
            match iteration :
                case 1 :
                    raw_name = input("Enter Full name: ").replace(" ", "_")
                    while True:
                            try:
                                date_of_birth = int(input("Enter your full date of birth (format: DDMMYYYY): ")) 
                                break
                            except ValueError: 
                                print("\nThe format is wrong. Try again:")
                    id_num = B1.creat_id(int(date_of_birth))
                    user_id = B1.creat_account(raw_name, date_of_birth, id_num)
                    name = raw_name
                    print("Account saved. The system will now remember your ID for the next session.")
                case 2 :
                    if name==None:
                        user_id = input("What is your user_id : ")
                        name, id_num = B1.get_user_infos(user_id)
                    if name != None and id_num != None:
                        B1.see_balance(name, id_num)
                case 3 :
                    if name==None:
                        user_id = input("What is your user_id : ")
                        name, id_num = B1.get_user_infos(user_id)
                    amount = float(input("What is the amount you want to deposit : "))
                    if name != None and id_num != None:
                        B1.deposit(name, id_num, amount)
                case 4 :
                    if name==None:
                        user_id = input("What is your user_id : ")
                        name, id_num = B1.get_user_infos(user_id)
                    amount = float(input("What is the amount you want to widthdraw : "))
                    if name != None and id_num != None:
                        B1.width_draw(name, id_num, amount)
                case 5 :
                    if name==None:
                        user_id = input("What is your user_id : ")
                        name, id_num = B1.get_user_infos(user_id)
                    if name != None and id_num != None:
                        B1.delete_account(name, id_num)
                case 6:
                    name = None
                    id_num = None
                    user_id = None
                case _ :
                    print("Invalid choice. Please try again.")
            status = input("\nDo you want to preform another operation? (Y/N): ")
            if status != "Y" and status != "y":
                break

B1 = bankaccount()
welcoming_software(B1)
