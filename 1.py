class Account:
    def __init__(self, number, owner, balance=0):
        if balance < 0:
            raise ValueError("Начальный остаток не может быть отрицательным")
        self.number = number
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount

    def __repr__(self):
        return f"Account({self.number!r}, {self.owner!r}, {self.balance})"


if __name__ == "__main__":
    acc = Account("40817", "Иван", 1000)
    acc.deposit(500)
    print(acc.balance)  
    acc.withdraw(200)
    print(acc.balance)   
    
    try:
        acc.withdraw(5000)
    except ValueError as e:
        print(f"ValueError: {e}")  
        
    print(acc.balance)   
    print(repr(acc))     
