
### Repository overview
This respository contains a Python script used to simulate a banking system capable of creating user accounts, withdrawals, deposits, money transfers, payments, and 2% cashbacks.
The application also keeps a historical record of transactions and prevents users from creating invalid or dangerous transactions (i.e. overdrafts, duplicate withdrawals, etc.). 
This application has gone through a series of tests to ensure its usability by business owners who may want to implement a purchasing or bank-like system.

### Repository contents
- banking_system_impl.py 
- main.py 
- Test cases folder containing unit tests in 4 .py files 
- Initial designs (pdf file).

### How to use
To use the banking system, the user will need to first ensure the `banking_system_impl.py` file and the `main.py` file are in the same file paths in their computer. Within the `main.py` , the user may find code that exists under `if __name__ == "__main__":`. This existing code is an example on how to use the banking system. The user may use this example as a guide or ignore it. 

To initialize the banking system, the user must assign `BankingSystemImpl()` to a variable name of their system. They can then use `Mybank.` followed by the name of the method they'd like the system to perform. It is recommended the user creates accounts first. The possible list of methods are as follows: 
- `create_account(self, timestamp: int, account_id: str)`
- `deposit(self, timestamp: int, account_id: str, amount: int)`
- `transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int)`
- `top_spenders(self, timestamp: int, n: int)`
- `pay(self, timestamp: int, account_id: str, amount: int)`
- `get_payment_status(self, timestamp: int, account_id: str, payment: str)`
- `merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str)`
- `get_balance(self, timestamp: int, account_id: str, time_at: int)`

### Data structures, algorithms, and libraries
- Data structures: Hash tables, arrays, lists. 
- Algorithms: Tim sort (altered version of merge sort).
- Libraries: Python standard library

### Contributors 
- Carmen Matar - [C-Matar] (https://github.com/C-Matar)
- Brandon T. Ton  - [brandontton](https://github.com/brandontton)
- Timothy E. Nguyen - [nguyen-timothy](https://github.com/nguyen-timothy)
- Joyce Yu - [joyceyu579](https://github.com/joyceyu579)