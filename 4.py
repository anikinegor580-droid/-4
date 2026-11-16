class Account:
    def __init__(self, number, owner, balance=0):
        if balance < 0:
            raise ValueError("Начальный остаток не может быть отрицательным")
        self.number = number
        self.owner = owner
        self._balance = balance
    @property
    def balance(self):
        return self._balance
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._balance += amount
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
    def __repr__(self):
        return f"Account({self.number!r}, {self.owner!r}, {self._balance})"
class SavingsAccount(Account):
    def __init__(self, number, owner, balance=0, rate=0.05):
        super().__init__(number, owner, balance)
        self.rate = rate

    def add_interest(self):
        self._balance += self._balance * self.rate

    def __repr__(self):
        return (
            f"SavingsAccount({self.number!r}, {self.owner!r}, "
            f"{self._balance}, {self.rate})"
        )


class CheckingAccount(Account):
    def __init__(self, number, owner, balance=0, overdraft=0):
        super().__init__(number, owner, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if self._balance - amount < -self.overdraft:
            raise ValueError("Превышен овердрафт")
        self._balance -= amount

    def __repr__(self):
        return (
            f"CheckingAccount({self.number!r}, {self.owner!r}, "
            f"{self._balance}, {self.overdraft})"
        )
if __name__ == "__main__":
    s = SavingsAccount("1", "Иван", 1000, rate=0.1)
    s.add_interest()
    print(s.balance)   
    print(repr(s))     

    try:
        s.withdraw(2000)
    except ValueError as e:
        print(f"ValueError: {e}")

    try:
        s.balance = 0
    except AttributeError:
        print("AttributeError: нельзя изменить balance напрямую")

    c = CheckingAccount("2", "Мария", 100, overdraft=500)
    c.withdraw(400)
    print(c.balance)   # -300

    try:
        c.withdraw(300)
    except ValueError as e:
        print(f"ValueError: {e}")

    c.deposit(1000)
    print(c.balance)   
    print(repr(c))     
    print(isinstance(c, Account))  
