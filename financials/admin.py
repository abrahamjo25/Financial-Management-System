from django.contrib import admin
from .models import Currency,ExpenseType,Expense,TaxType,Sales,Banks
from .forms import ExpenseForm,SalesForm
# Register your models here.
admin.site.register(Currency)

class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('expenseName', 'description')  # Specify the fields to display in the tabular format
admin.site.register(ExpenseType,ExpenseTypeAdmin)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('expenseName', 'description')

admin.site.register(TaxType)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("get_expense_name", "nameOfRecipient", "totalAmount","beforeVAT","VATTotal","vatType", "fsNO", "wth", "net", "recipientType", "projectName", "remark")
    form = ExpenseForm  # Use the custom form for Expense

    def get_expense_name(self, obj):
        return obj.expenseType.expenseName

    get_expense_name.short_description = 'Expense Type'  # Set custom header name

admin.site.register(Expense, ExpenseAdmin)

class SalesAdmin(admin.ModelAdmin):
    list_display = ("nameOfProject", "amount","get_currency_name",  "fsNumber", "remark")
    form = SalesForm  # Use the custom form for Sales
    def get_currency_name(self, obj):
        return obj.currencyType.currencySymbol
    get_currency_name.short_description = 'Currency'  # Set custom header name
admin.site.register(Sales,SalesAdmin)

class BankAdmin(admin.ModelAdmin):
    list_display = ("bankName", "initial","get_currency_name")
    form = SalesForm  # Use the custom form for Sales
    def get_currency_name(self, obj):
        return obj.currencyType.currencySymbol
    get_currency_name.short_description = 'Currency'  # Set custom header name
admin.site.register(Banks,BankAdmin)

from .utils import BalanceSheet  # Assuming you put the BalanceSheet class in a utils module

class BalanceSheetAdmin(admin.ModelAdmin):
    readonly_fields = ('bank_balance', 'pending_expenses')
    actions = ['generate_balance_sheet']

    def bank_balance(self, obj):
        return BalanceSheet.calculate_bank_balance()

    def pending_expenses(self, obj):
        return BalanceSheet.calculate_pending_expenses()

    def generate_balance_sheet(self, request, queryset):
        bank_balance, pending_expenses = BalanceSheet.generate_balance_sheet()
        self.message_user(request, f"Bank Balance: {bank_balance}, Pending Expenses: {pending_expenses}")

    bank_balance.short_description = 'Bank Balance'
    pending_expenses.short_description = 'Pending Expenses'
    generate_balance_sheet.short_description = 'Generate Balance Sheet'

