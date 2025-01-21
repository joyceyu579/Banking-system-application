class BankingSystemImpl():

    def __init__(self):
        self.accounts = {}
        self.payment_inc = 0
        self.payments = {}
        self.balance_history = {}

        # self.accounts = {account_id : (amount, timestamp, transferred, payment_tracker)}
        # self.payments = {account_id_2 : [(payment0, 0, 0), (payment1, cashback, waiting_period), (payment2, cashback, waiting_period)]}
        # self.balance_history = {account_id : [(timestamp, balance), ...]}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Should create a new account with the given identifier if it
        doesn't already exist.
        Returns `True` if the account was successfully created or
        `False` if an account with `account_id` already exists.
        """
        if account_id not in self.accounts:

            amount = 0
            transferred = 0
            payment_tracker = 0
            self.accounts[account_id] = [amount, timestamp, transferred, payment_tracker]
            
            # Every account has payment information.
            payment_id = "payment0"
            cashback = 0
            waiting_period = 0
            self.payments[account_id] = [(payment_id, cashback, waiting_period)]
            self.balance_history[account_id] = [(timestamp, amount)]

            return True
        else:
            return False
        
    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Should deposit the given `amount` of money to the specified
        account `account_id`.
        Returns the balance of the account after the operation has
        been processed.
        If the specified account doesn't exist, should return
        `None`.
        """
        # Check for any pending cashbacks
        if account_id in self.accounts.keys():
            for i in range(len(self.payments[account_id])):
                if timestamp >= self.payments[account_id][i][2]:
                    if self.payments[account_id][i][1] > 0:
                        self.accounts[account_id][0] += self.payments[account_id][i][1]
                        self.payments[account_id][i] = (self.payments[account_id][i][0], 0, self.payments[account_id][i][2]) # set cashback value to 0 after processing it.
                        
            #MAKE DEPOSITS   
            self.accounts[account_id][0] += amount
            self.accounts[account_id][1] = timestamp
            self.balance_history[account_id].append((timestamp, self.accounts[account_id][0]))

            return self.accounts[account_id][0]
        else:
            return None

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        """
        Should transfer the given amount of money from account
        `source_account_id` to account `target_account_id`.
        Returns the balance of `source_account_id` if the transfer
        was successful or `None` otherwise.
          * Returns `None` if `source_account_id` or
          `target_account_id` doesn't exist.
          * Returns `None` if `source_account_id` and
          `target_account_id` are the same.
          * Returns `None` if account `source_account_id` has
          insufficient funds to perform the transfer.
        """
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        elif source_account_id == target_account_id:
            return None
        elif self.accounts[source_account_id][0] < amount:
            return None
        else:
            self.accounts[source_account_id][0] -= amount
            self.accounts[target_account_id][0] += amount

            self.accounts[source_account_id][1] = timestamp
            self.accounts[target_account_id][1] = timestamp
            self.accounts[source_account_id][2] += amount

            self.balance_history[source_account_id].append((timestamp, self.accounts[source_account_id][0]))
            self.balance_history[target_account_id].append((timestamp, self.accounts[target_account_id][0]))

            return self.accounts[source_account_id][0]
        
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        """
        Should return the identifiers of the top `n` accounts with
        the highest outgoing transactions - the total amount of
        money either transferred out of or paid/withdrawn (the
        **pay** operation will be introduced in level 3) - sorted in
        descending order, or in case of a tie, sorted alphabetically
        by `account_id` in ascending order.
        The result should be a list of strings in the following
        format: `["<account_id_1>(<total_outgoing_1>)", "<account_id
        _2>(<total_outgoing_2>)", ..., "<account_id_n>(<total_outgoi
        ng_n>)"]`.
          * If less than `n` accounts exist in the system, then return
          all their identifiers (in the described format).
          * Cashback (an operation that will be introduced in level 3)
          should not be reflected in the calculations for total
          outgoing transactions.
        """
        list_of_sorted = []
        sorted_accounts = dict(sorted(self.accounts.items(), key=lambda x: (-x[1][2], x[0])))
        for k, v in sorted_accounts.items():
            list_of_sorted.append(f"{k}({v[2]})")

        if n <= len(list_of_sorted):

            return list_of_sorted[:n]
        else:
            return list_of_sorted
        
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        """
        Should withdraw the given amount of money from the specified
        account.
        All withdraw transactions provide a 2% cashback - 2% of the
        withdrawn amount (rounded down to the nearest integer) will
        be refunded to the account 24 hours after the withdrawal.
        If the withdrawal is successful (i.e., the account holds
        sufficient funds to withdraw the given amount), returns a
        string with a unique identifier for the payment transaction
        in this format:
        `"payment[ordinal number of withdraws from all accounts]"` -
        e.g., `"payment1"`, `"payment2"`, etc.
        Additional conditions:
          * Returns `None` if `account_id` doesn't exist.
          * Returns `None` if `account_id` has insufficient funds to
          perform the payment.
          * **top_spenders** should now also account for the total
          amount of money withdrawn from accounts.
          * The waiting period for cashback is 24 hours, equal to
          `24 * 60 * 60 * 1000 = 86400000` milliseconds (the unit for
          timestamps).
          So, cashback will be processed at timestamp
          `timestamp + 86400000`.
          * When it's time to process cashback for a withdrawal, the
          amount must be refunded to the account before any other
          transactions are performed at the relevant timestamp.
        """
        # self.accounts = {account_id : (amount, timestamp, transferred, payment_tracker)}
        # self.payments = {account_id_2 : [(payment0, 0, 0), (payment1, cashback, waiting_period), (payment2, cashback, waiting_period)]}

        if account_id not in self.accounts:
            return None
        
        if account_id in self.accounts.keys():
            for i in range(len(self.payments[account_id])):
                if timestamp >= self.payments[account_id][i][2]:
                    if self.payments[account_id][i][1] > 0:
                        self.accounts[account_id][0] += self.payments[account_id][i][1]
                        self.payments[account_id][i] = (self.payments[account_id][i][0], 0, self.payments[account_id][i][2])
                        
        if self.accounts[account_id][0] < amount:
            return None
            
        # creates unique payment 
        self.payment_inc += 1
        payment_string = f"payment{self.payment_inc}"
        self.accounts[account_id][3] = self.payment_inc

        # withdrawal of moneys
        self.accounts[account_id][0] -= amount
        self.accounts[account_id][1] = timestamp
        self.accounts[account_id][2] += amount

        # update payment info
        cashback = amount // 50

        waiting_period = 86400000 + timestamp

        self.payments[account_id].append((payment_string, cashback, waiting_period))

        self.balance_history[account_id].append((timestamp, self.accounts[account_id][0]))

        return f"payment{self.payment_inc}"

    
    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        """
        Should return the status of the payment transaction for the
        given `payment`.
        Specifically:
          * Returns `None` if `account_id` doesn't exist.
          * Returns `None` if the given `payment` doesn't exist for
          the specified account.
          * Returns `None` if the payment transaction was for an
          account with a different identifier from `account_id`.
          * Returns a string representing the payment status:
          `"IN_PROGRESS"` or `"CASHBACK_RECEIVED"`.
        """
        if account_id not in self.accounts:
            return None
        for payments in self.payments[account_id]:
            if payments[0] == payment:
                if payments[2] > timestamp:
                    return "IN_PROGRESS"
                else:
                    return "CASHBACK_RECEIVED"
        return None
    
    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        """
        Should merge `account_id_2` into the `account_id_1`.
        Returns `True` if accounts were successfully merged, or
        `False` otherwise.
        Specifically:
          * Returns `False` if `account_id_1` is equal to
          `account_id_2`.
          * Returns `False` if `account_id_1` or `account_id_2`
          doesn't exist.
          * All pending cashback refunds for `account_id_2` should
          still be processed, but refunded to `account_id_1` instead.
          * After the merge, it must be possible to check the status
          of payment transactions for `account_id_2` with payment
          identifiers by replacing `account_id_2` with `account_id_1`.
          * The balance of `account_id_2` should be added to the
          balance for `account_id_1`.
          * `top_spenders` operations should recognize merged accounts
          - the total outgoing transactions for merged accounts should
          be the sum of all money transferred and/or withdrawn in both
          accounts.
          * `account_id_2` should be removed from the system after the
          merge.
        """
        if account_id_1 == account_id_2:
            return False
        
        if account_id_1 not in self.accounts or account_id_2 not in self.accounts:
            return False

        # All pending cashback refunds for `account_id_2` should still be processed, but refunded to `account_id_1` instead.
        for i in range(len(self.payments.get(account_id_2))):
            if timestamp >= self.payments[account_id_2][i][2] and self.payments[account_id_2][i][1] > 0:
                self.accounts[account_id_1][0] += self.payments[account_id_2][i][1]
                self.payments[account_id_2][i] = (self.payments[account_id_2][i][0], 0, self.payments[account_id_2][i][2]) # set cashback value to 0 after processing it.

        # The balance of `account_id_2` should be added to the balance for `account_id_1`.
        self.accounts[account_id_1][0] += self.accounts[account_id_2][0] # transfer amount over 
        self.accounts[account_id_1][2] += self.accounts[account_id_2][2] # transfer withdrawal/transferred amount over  
        
        if account_id_2 in self.payments:
            self.payments[account_id_1].extend(self.payments[account_id_2])

        del self.payments[account_id_2]
        del self.accounts[account_id_2]

        self.balance_history[account_id_1].append((timestamp, self.accounts[account_id_1][0]))
        self.balance_history[account_id_2].append((timestamp, None))
        return True
        

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        """
        Should return the total amount of money in the account
        `account_id` at the given timestamp `time_at`.
        If the specified account did not exist at a given time
        `time_at`, returns `None`.
          * If queries have been processed at timestamp `time_at`,
          `get_balance` must reflect the account balance **after** the
          query has been processed.
          * If the account was merged into another account, the merged
          account should inherit its balance history.
        """
        if account_id not in self.accounts and account_id not in self.balance_history:
            return None
        
        self.deposit(time_at, account_id, 0)

        balances_new = []
        for balance in self.balance_history[account_id]:
            if balance[0] <= time_at:
                balances_new.append(balance)
            else:
                break
        
        if len(balances_new) == 0:
            return None
        
        return balances_new[-1][1]
        

