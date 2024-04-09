from django.shortcuts import render
from django.db.models import Sum  # Import Sum

from financials import models
from financials.models import Banks, Expense, Sales
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    if request.user.is_superuser:
        total_sales = Sales.objects.aggregate(total_sales=Sum('amount'))['total_sales'] or 0

        # Calculate total expenses amount
        total_expenses = Expense.objects.aggregate(total_expenses=Sum('totalAmount'))['total_expenses'] or 0

        # Calculate total balance
        net_income = total_sales - total_expenses

        latest_activities = LogEntry.objects.all().order_by('-action_time')[:10]

        users =  User.objects.count()
        banks = Banks.objects.all()

        total_balance = 0
        initial_sum = Banks.objects.aggregate(total_balance=Sum('initial'))['total_balance']
        if initial_sum:
            total_balance = initial_sum

        # Calculate percentage for each bank
        for bank in banks:
            if total_balance > 0:
                bank.percentage = (bank.initial / total_balance) * 100
            else:
                bank.percentage = 0

        context = {
            'net_income':net_income,
            'total_balance': total_balance,
            'total_sales': total_sales,
            'total_expenses': total_expenses,
            'banks': banks,
            'users':users,
            'latest_activities':latest_activities,
        }
        return render(request, 'pages/index.html', context)
    else:
        return render(request, 'pages/guest.html')
