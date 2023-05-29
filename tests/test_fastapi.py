from app.calculations import add, BankAccount
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def initial_bank_account():
    return BankAccount(100)

@pytest.mark.parametrize("num1, num2, ans",
                         [(3,10,13),
                         (2,7,9),
                         (12, 4, 16)])
def test_add(num1, num2, ans):
    print('testing add function')

    assert add(num1, num2) == ans


def test_bank_initial_amount(initial_bank_account):
    # bank_acc = BankAccount(100)

    assert initial_bank_account.balance == 100

def test_bank_default_amount(zero_bank_account):
    # bank_acc = BankAccount()
    assert zero_bank_account.balance == 0

def test_deposit(initial_bank_account):
    # bank_acc = BankAccount(initial_bank_account)
    initial_bank_account.deposit(100)
    assert initial_bank_account.balance == 200

def test_withdraw(initial_bank_account):
    # bank_acc = BankAccount(100)
    initial_bank_account.withdraw(50)
    assert initial_bank_account.balance == 50

def test_interest(initial_bank_account):
    # bank_acc = BankAccount(100)
    initial_bank_account.collect_interest()
    assert round(initial_bank_account.balance, 2) == 110


def test_insufficent_funds(initial_bank_account):
    with pytest.raises(Exception):
        initial_bank_account.withdraw(200)
