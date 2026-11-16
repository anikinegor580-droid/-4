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


class Customer:
    def __init__(self, name, customer_id):
        self.name = name
        self.customer_id = customer_id
        self._accounts = []

    def add_account(self, account):
        self._accounts.append(account)

    def remove_account(self, number):
        for i, acc in enumerate(self._accounts):
            if acc.number == number:
                del self._accounts[i]
                return
        raise KeyError(f"Счёт {number!r} не найден у клиента")

    def accounts(self):
        return list(self._accounts)

    def total_balance(self):
        return sum(acc.balance for acc in self._accounts)


class Bank:
    def __init__(self):
        self._customers = {}
        self._accounts = {}

    def add_customer(self, customer):
        if customer.customer_id in self._customers:
            raise ValueError(f"Клиент с ID {customer.customer_id!r} уже существует")
        self._customers[customer.customer_id] = customer

    def customer(self, customer_id):
        if customer_id not in self._customers:
            raise KeyError(f"Клиент с ID {customer_id!r} не найден")
        return self._customers[customer_id]

    def open_account(self, customer_id, account):
        cust = self.customer(customer_id)
        if account.number in self._accounts:
            raise ValueError(f"Счёт с номером {account.number!r} уже существует")
        self._accounts[account.number] = (account, customer_id)
        cust.add_account(account)

    def close_account(self, number):
        if number not in self._accounts:
            raise KeyError(f"Счёт с номером {number!r} не найден")
        account, customer_id = self._accounts[number]
        if account.balance != 0:
            raise ValueError("Нельзя закрыть счёт с ненулевым остатком")
        del self._accounts[number]
        self._customers[customer_id].remove_account(number)

    def transfer(self, from_number, to_number, amount):
        if from_number not in self._accounts or to_number not in self._accounts:
            raise KeyError("Один или оба счёта не найдены")
        if from_number == to_number:
            raise ValueError("Нельзя перевести деньги на тот же счёт")

        from_acc, _ = self._accounts[from_number]
        to_acc, _ = self._accounts[to_number]

        from_acc.withdraw(amount)
        to_acc.deposit(amount)

    def accounts(self, customer_id, min_balance=None):
        cust = self.customer(customer_id)
        cust_accounts = cust.accounts()
        if min_balance is None:
            return cust_accounts
        return [acc for acc in cust_accounts if acc.balance >= min_balance]

    def total_deposits(self):
        return sum(acc.balance for acc, _ in self._accounts.values())
