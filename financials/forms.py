from django import forms
from .models import Expense,ExpenseType,Sales,Currency,Banks

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the queryset and widget for the expenseType field
        self.fields['expenseType'].queryset = ExpenseType.objects.all()
        self.fields['expenseType'].widget = forms.Select(choices=[(exp.id, exp.expenseName) for exp in ExpenseType.objects.all()])
        self.fields['bank_account'].queryset = Banks.objects.all()
        self.fields['bank_account'].widget = forms.Select(choices=[(exp.id, exp.bankName) for exp in Banks.objects.all()])
class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['currencyType'].queryset = Currency.objects.all()
        self.fields['currencyType'].widget = forms.Select(choices = [(cur.id, cur.currencySymbol) for cur in Currency.objects.all()])
        self.fields['bank_account'].queryset = Banks.objects.all()
        self.fields['bank_account'].widget = forms.Select(choices=[(exp.id, exp.bankName) for exp in Banks.objects.all()])