import datetime
import random
from string import digits
import uuid
from dataclasses import dataclass


@dataclass
class Customer:

    history = dict()
    trans_id = 0

    firstname:str
    lastname:str
    email:str
    phonenumber:int
    dateofbirth:datetime
    __balance = 0
    
    transaction = []


    def __str__(self) -> str:
        fullname = f'{self.firstname} {self.lastname}'
        fullname = lambda first, last: first + " " + last
        return f'{fullname(self.firstname, self.lastname)} \t {self.email} \t {self.phonenumber} \t {self.dateofbirth}'
    

    def updateBalance(self, type, amount):
        if type == 'deposit':
            self.__balance += amount
        elif type == 'withdrawal':
            if self.__balance <= amount:
                print('Insufficinet fund to withdraw')
            else:
                self.__balance -= amount
        
        elif type == 'transfer':
            if self.__balance <= amount:
                print("Insufficient funds to transfer")
            else:
                recipient = input("Enter recipient's account number:  ")
                self.__balance -= amount

        else:
            print('Invalid')
            return
        
        self.transaction.append({"type": type, "amount": amount, "balance": self.__balance, "time":datetime()})



    @classmethod 
    def updateHistory(cls, date, type, amount):
            accountNumber = random.choices(digits, k=10)
            cls.__setattr__("account_number", accountNumber)
            cls.history[f"{date}"] = {"type": type, "amount": amount, "balance": cls.balance}


    def getBalance(self):
        return self.__balance
    
    def viewHistory(self):
        history = ""
        for transadate, details in self.history.items():
            history += f"{transadate} \t {details['type']} \t {details['amount']} \t {details['balance']}\n"
        print(history)
        return history
    
    def generateAccount(self):
        while True:
            accountNumber = str(uuid.uuid4().int)[:10]
            if accountNumber not in Bank.customers:
                self.__setattr__("account_number", accountNumber)
                return self.account_number
            
@dataclass
class Bank:
    bankName = "Polar Bank"

    customers = {}    
    balance: int = 0    
    username = {}     
    def deposit(self, account, amount):
        customer = self.customers[account]
        customer.updateBalance("deposit", amount)

    def withdrawal(self, account, amount):
        customer = self.customers[account]
        customer.updateBalance("withdrawal", amount)

    def transfer(self, account, amount):
        customer = self.customers[account]
        customer.updateBalance("transfer", amount)

    def viewHistory(self, account):
        if account in self.customers:
            customer = self.customers[account]
            customer.viewHistory()
        else:
            print("no history")


#for customer to Signup 
@classmethod
def signUp(cls, firstName, lastName, phoneNo, email, dateOfBirth):
        
        customer = Customer(firstName, lastName, phoneNo, email, dateOfBirth,)
        accountNumber = customer.generateAccount()
        cls.customers[f'{accountNumber}'] = customer
        return customer

@classmethod
def login(cls, det):
        email = input("Email:  ")
        password = input("Password:  ")

        if email in det and password in det:
            print("\nLogin successful")
            return True
        else:
            print("\nInvalid")
            return False


if __name__ == '__main__':
    running = True  
    transact = False    
    polarBank = Bank() 
    loginDetail = []   
    print("\n")
    print("WELCOME TO POLARBANK")

    while running:
        print("\nPress a number between 1 and 7 \n")
        operation = input(
            "1. Sign-up \n2. Check Account Balance \n3. Deposit \n4. Withdrawal \n5. Transfer \n6. Transaction History \n7. Exit \n") 

        if operation not in "1234567": 
            print("\nPlease enter a number between 1 and 7")
            continue
        else:
            if operation == "1":
                transact = True
                while transact:
                    email = input("Email:  ") 
                    if email in loginDetail:  
                        print("\n please login")
                        break
                    loginDetail.append(email) 
                    firstName = input("First Name:  ") 
                    lastName = input("Last Name:  ")   
                    phoneNo = input("Phone Number: ")   
                    dateOfBirth = input("Date of Birth:  ") 
                    password = input("Password:  ") 
                    loginDetail.append(password)   
                    balance = int(input("Opening Balance (min: #1000):  ")) 

                    try:    
                        if len(firstName) > 3 and len(lastName) > 3 and len(phoneNo) > 3 and ("@" in email) and dateOfBirth > 3 and balance:
                            if balance >= 1000: 
                                customer = Customer(
                                    firstName, lastName, phoneNo, email, balance) 
                                accountNumber = customer.generateAccount()  
                                if accountNumber:  
                                    polarBank.customers.update(
                                        {accountNumber: customer}) 
                                    
                                    print(f"\nCongratulations {firstName} {lastName}! Account created successfully. Your account number is {accountNumber}.")
                                    print("\n", polarBank.customers.items())
                                    polarBank.deposit(accountNumber, balance) 
                                    print(f"\nYour account has been credited with #{balance}. Your current balance is #{customer.getBalance}")
                                    print("\nPlease login to continue")
                                    transact = False    
                                    break  

                            else:
                                print("Minimum opening amount: #1000")
                                continue
                        else:
                            print("Invalid entry. Please try again")
                            continue
                    except ValueError:
                        print("Invalid entry")
                        break
            
            
            # Check balance
            elif operation == "2":  
                transact = True
                if not polarBank.login(loginDetail): 
                    continue
                while transact:
                    print("\nPress 0 to cancel\n")
                    accountNumber = input("Enter your account number:  ")
                    if accountNumber == "0":
                        transact = False
                        break
                    if accountNumber in polarBank.customers.keys(): 
                        print(f"\nYour account balance is #{polarBank.customers[accountNumber].getBalance}")
                        transact = False
                        break
                    else:
                        print("Invalid account number")
                        continue
            
            # Deposit
            elif operation == "3":  
                transact = True
                if not polarBank.login(loginDetail): 
                    continue
                while transact:
                    print("\nPress 0 to cancel\n")
                    accountNumber = input("Enter your account number:  ")  
                    if accountNumber == "0":
                        transact = False
                        break
                    customer = polarBank.customers[accountNumber]  
                    print("\n", customer)
                    if customer:
                        amount = int(input("Amount:  "))  
                        if amount:
                            polarBank.deposit(accountNumber, amount) 
                            print(f"\nYour account has been credited with #{amount}. Your current balance is #{customer.getBalance}")
                            print("\nTransaction completed.")
                            transact = False  
                            break   
                        else:
                            print("Invalid amount. Please try again")  
                            continue   
                    else:
                        print("Invalid! Please try again")  
                        continue  


            # Withdrawal
            elif operation == "4":  
                transact = True 
                if not polarBank.login(loginDetail): 
                    continue   
                while transact:
                    print("\nPress 0 to cancel\n")  
                    accountNumber = input("Account Number:  ")
                    if accountNumber == "0":    
                        transact = False
                        break
                    customer = polarBank.customers[accountNumber]
                    print("\n", customer)
                    if customer:
                        amount = int(input("Amount:  "))   
                        if amount:  
                            polarBank.withdrawal(accountNumber, amount)  
                            print(f"\nYour account has been debited with #{amount}. Your current balance is #{customer.getBalance}") 
                            print("\nTransaction completed.")
                            transact = False   
                            break 
                        else:
                            print("Invalid amount. Please try again") 
                            continue 
          
             # Transfer
            elif operation == "5": 
                transact = True 
                if not polarBank.login(loginDetail): 
                    continue   
                while transact: 
                    print("\nPress 0 to cancel\n")  
                    accountNumber = input("Account Number:  ")
                    if accountNumber == "0":    
                        transact = False  
                        break   
                    customer = polarBank.customers[accountNumber]
                    print(customer) 
                    if customer:    
                        amount = int(input("Amount:  ")) 
                        if amount:  
                            polarBank.transfer(accountNumber, amount)
                            print(f"\nYour account has been debited with #{amount}. Your current balance is #{customer.getBalance}")
                            print("\nTransaction completed")  
                            transact = False 
                            break  
                        else:
                            print(
                                "Invalid amount. Transaction failed. Please try again")
                            continue   

            # View transaction history
            elif operation == "6":  
                transact = True 
                if not polarBank.login(loginDetail):  
                    continue    
                while transact: 
                    userEntry = int(input("Account Number:  "))
                    customer = polarBank.customers[accountNumber] 
                    print(customer) 
                    if customer:    
                        polarBank.viewHistory(accountNumber) 
                        transact = False  
                        break  

            # to exit
            elif operation == "7":   
                transact = False  
                print("\nThank you for banking with us.")
                break   

