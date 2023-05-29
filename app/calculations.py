def add(num1: int, numb2: int):
    return num1 + numb2


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount: int):
        self.balance += amount

    def withdraw(self, amount: int):
        if amount > self.balance:
            raise Exception('Insufficient funds in account')
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1