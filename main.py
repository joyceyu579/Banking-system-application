from banking_system_impl import *

if __name__ == "__main__":
    MyBank = BankingSystemImpl() # create bank 
    
    # Create accounts
    MyBank.create_account(1, 'account1')
    MyBank.create_account(2, 'account2')
    MyBank.create_account(3, 'account3')

    # Making a deposit.
    MyBank.deposit(4, 'account1', 2500)
    MyBank.deposit(5, 'account2', 1000)

    # Transfer money between accounts.
    MyBank.transfer(5, 'account1', 'account2', 900)
    MyBank.transfer(7, 'account2', 'account3', 100)

    # Reporting all accounts sorted from top to least spenders.
    # Spending defined as withdrawals + transfers + payments.
    MyTopSpenders = MyBank.top_spenders(10, 3)
    print(MyTopSpenders)

    # Making and tracking a payment.
    MyBank.pay(11, 'account1', 100) 
    MyBank.deposit(86400010, 'account1', 100)

    # Check current balance and successful cashback made on payment:
    print(MyBank.get_balance(15, 'account1', 14))

    # Check previous at a certain time in the past for specific accounts:
    print(MyBank.get_balance(16, 'account1', 10))

    # Merge accounts:
    MyBank.merge_accounts(17, 'account1', 'account2')



