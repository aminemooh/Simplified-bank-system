import math
import sqlite3
from abc import ABC, abstractmethod
from Ceaser import Caesar
from Vigenere import VigenereCipher
from rsaforbank import RSA_manager
class Bank(ABC):
    @abstractmethod
    def creat_account():
        pass
    @abstractmethod
    def width_draw():
        pass
    @abstractmethod
    def see_balance():
        pass
    @abstractmethod
    def deposit():
        pass
    @abstractmethod
    def delete_account():
        pass

class bankaccount(Bank):
    def __init__(self):
        self.db = 'bank.db'
        self.rsa = RSA_manager()
        self.vc = VigenereCipher("RLKG")
        self.cc = Caesar(7)
        
    def creat_id(self, birthdate_int):
        val = math.pow(birthdate_int, 2) 
        trig_component = abs(math.sin(birthdate_int) * 1000000)
        stable_base = math.isqrt(int(val))
        mixed_id = (stable_base + trig_component) * math.log10(birthdate_int)
        id_num = math.floor(mixed_id) % 100000000
        return id_num #the formula is floor([|sin(n)*10^6| + floor_sqrt(n**2)]*log10(n)) % 10^6 the mode is to insure it's under 6 digits long 
    
    def creat_account(self, name, date_of_birth, id_num):
        en = self.cc.encrypt(self.vc.encrypt(name))
        eid = self.rsa.encrypt_rsa(self.rsa ,id_num)
        user_id = en + "-" + str(eid) #creating the user_id given to the user to open his account
        conn = sqlite3.connect(self.db) #opening the database
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT,
                id_num INTEGER,
                balance REAL DEFAULT 0.0,
                type_of_customer BOOLEAN,
                UNIQUE(name, id_num)
            )
        ''') #creating a table (if not already created) to store the users' data
        type_c = input("Are you willing to make a donation to the bank? (Y/N) : ") #verfying if the user is a VIP member
        type_c = 1 if type_c == "Y" or type_c == "y" else 0
        user = (name, date_of_birth, id_num, 0, type_c)
        try:
            cursor.execute('''
                INSERT INTO accounts (name, date_of_birth, id_num, balance, type_of_customer) 
                VALUES (?, ?, ?, ?, ?)
                ''', user)
            conn.commit()
            print(f"Account successfully created! ID: {user_id}")
        except sqlite3.IntegrityError:
            print("Error: An account with this name/ID already exists.")
        conn.close() #closing the database
        return user_id
    def see_balance(self, name, id_num):
        conn = sqlite3.connect(self.db)
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE name = ? AND id_num = ?", (name, id_num))
        result = cursor.fetchone()
        conn.close()
        if result:
            print(f"Your Account's Balance is : {result[0]}")
        else:
            print("User not found or ID/Name mismatch.")
    def deposit(self, name, id_num, amount):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT balance, type_of_customer FROM accounts WHERE name = ? AND id_num = ?",(name, id_num))
        result = cursor.fetchone()
        if result:
            current_balance, type_of_customer = result
            if type_of_customer:  #check if special customer 
                new_balance = current_balance + amount   # no interest
            else:
                new_balance = current_balance + amount - (amount*0.01)  # normal interest
            cursor.execute("UPDATE accounts SET balance = ? WHERE name = ? AND id_num = ?",(new_balance, name, id_num))
            conn.commit()
            print("Done! Balance updated.")
        else:
            print("User not found.")
        conn.close()
    def width_draw(self,name, id_num,amount):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT balance, type_of_customer FROM accounts WHERE name = ? AND id_num = ?",(name, id_num))
        result = cursor.fetchone()
        if result:
            current_balance, type_of_customer = result
            if current_balance >= amount:
                if type_of_customer:  #check if special customer 
                    new_balance = current_balance - amount   # no interest
                else:
                    new_balance = current_balance - (amount * 1.01)  # normal interest 0.01%

                cursor.execute("UPDATE accounts SET balance = ? WHERE name = ? AND id_num = ?",(new_balance, name, id_num))
                conn.commit()
                print("Done! Balance updated.")

            else:
                print("Not enough money.")
                i = input("Do you want to withdraw a loan (Y/N): ")

                if i.lower() == "y":
                    loan_limit = -500000.0 if type_of_customer else -100000.0 #loan limit
                    if current_balance > loan_limit:
                        if type_of_customer:
                            new_balance = current_balance - amount #no loan for vip costumers
                        else:
                            new_balance = current_balance - (amount * 1.01) #1% intrest for operation
                            new_balance -= abs(new_balance) * 0.05 #intrest for the loan 5%
                        cursor.execute("UPDATE accounts SET balance = ? WHERE name = ? AND id_num = ?",(new_balance, name, id_num))
                        conn.commit()
                        print("Done! Balance updated.")
                    else:
                        print("Your current balance is too low, pay off your debt first...")

        else:
            print("User not found.")
        conn.close()
                
    def delete_account(self, name, id_num):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE name = ? AND id_num = ?", (name, id_num))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Successfully deleted account for {name}.")
        else:
            print("No matching account found to delete.")
        conn.close()
    def get_user_infos(self,user_id):
        while True :
            try:
                en, eid = user_id.split("-") #separating the name and id_num to get user informations from the database
                name = self.vc.decrypt(self.cc.decrypt(en)) 
                id_num = self.rsa.decrypt_rsa(eid) 
                return name, id_num
            except Exception: #in case of wronge format
                print("Error: Invalid User ID format or decryption failed.")
                i = input("Do you want to try again ? (Y/N) : ")
                if i == "Y" or i == "y" :
                    user_id = input("What is your user_id : ")
                    return self.get_user_infos(user_id)
                else:
                    return None, None   
