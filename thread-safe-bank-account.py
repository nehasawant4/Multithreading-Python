import threading

class BankAccount:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self, amount):
        self.lock.acquire()
        try:
            self.balance += amount
        finally:
            self.lock.release()

    def withdraw(self, amount):
        self.lock.acquire()
        try:
            if amount < self.balance:
                self.balance -= amount
            else:
                print("Insufficient balance")
        finally:
            self.lock.release()

    def get_balance(self):
        self.lock.acquire()
        try:
            return self.balance
        finally:
            self.lock.release()

def deposit_many(account, times, amount):
    for _ in range(times):
        account.deposit(amount)

def withdraw_many(account, times, amount):
    for _ in range(times):
        account.withdraw(amount)  

def main():
    account = BankAccount()

    t1 = threading.Thread(target=deposit_many, args=(account, 10, 100))
    t2 = threading.Thread(target=deposit_many, args=(account, 10, 100))

    t3 = threading.Thread(target=withdraw_many, args=(account, 10, 50))
    t4 = threading.Thread(target=withdraw_many, args=(account, 10, 50))

    threads = [t1, t2, t3, t4]

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

    print("Balance: ", account.get_balance())

if __name__ == "__main__":
    main()