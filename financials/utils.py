from financials.models import Banks, Expense


class BalanceSheet:
    @classmethod
    def calculate_bank_balance(cls):
        bank_balance = sum(Banks.objects.values_list('initial', flat=True))
        return bank_balance

    @classmethod
    def calculate_pending_expenses(cls):
        pending_expenses = sum(Expense.objects.values_list('totalAmount', flat=True))
        return pending_expenses

    @classmethod
    def generate_balance_sheet(cls):
        bank_balance = cls.calculate_bank_balance()
        pending_expenses = cls.calculate_pending_expenses()
        return bank_balance, pending_expenses