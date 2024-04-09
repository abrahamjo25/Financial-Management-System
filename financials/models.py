from django.db import models

class Currency(models.Model):
    currencySymbol = models.CharField(max_length=10, verbose_name='Currency Code')
    currencyName = models.CharField(max_length=100, verbose_name='Currency Name')
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.currencySymbol} ({self.currencyName})"
    
    class Meta:
        verbose_name_plural = "Currencies"

class ExpenseType(models.Model):
    expenseName = models.CharField(max_length=100, verbose_name='Expense Name')
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expenseName} ({self.description})"
    
    class Meta:
        verbose_name_plural = "Expense Types"

class TaxType(models.Model):
    vatName = models.CharField(max_length=200, verbose_name='Tax Name')  
    rate = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='Rate(%)')
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vatName} ({self.rate}%)"
    
    class Meta:
        verbose_name_plural = "Tax Types"

class Banks(models.Model):
    bankName = models.CharField(max_length=100, verbose_name='Name of Bank')
    initial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    currencyType = models.ForeignKey(Currency, verbose_name='Currency', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Banks"
class Expense(models.Model):
    expenseType = models.ForeignKey(ExpenseType, on_delete=models.CASCADE, verbose_name='Expense Type')
    nameOfRecipient = models.CharField(max_length=200, verbose_name='Recipient Name')
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Amount')
    bank_account = models.ForeignKey(Banks, on_delete=models.CASCADE, verbose_name='Debited Account')
    beforeVAT = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Before VAT', editable=False)
    vatType = models.ForeignKey(TaxType, related_name='expenses_vat', on_delete=models.CASCADE, verbose_name='VAT Type')
    VATTotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='VAT Total', editable=False)
    wthType = models.ForeignKey(TaxType, related_name='expenses_wth', on_delete=models.CASCADE, verbose_name='WTH Type')
    wth = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='WTH', editable=False)
    net = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Net', editable=False)
    fsNO = models.CharField(max_length=10, verbose_name='FS No')
    RECIPIENT_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Company', 'Company'),
    ]
    recipientType = models.CharField(max_length=200, verbose_name='Recipient Type', choices=RECIPIENT_TYPE_CHOICES)
    projectName = models.CharField(max_length=200, verbose_name='Project Name')
    remark = models.TextField(verbose_name='Remark')
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate beforeVAT, VATTotal, WTH, and net before saving
        self.beforeVAT = self.totalAmount / (1 + self.vatType.rate / 100)
        self.VATTotal = self.totalAmount - self.beforeVAT
        self.wth = self.totalAmount * (self.wthType.rate / 100)
        self.net = self.totalAmount - self.wth
        # Debit the bank account
        self.bank_account.initial -= self.net
        self.bank_account.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Rollback bank account transaction
        self.bank_account.initial += self.net
        self.bank_account.save()
        super().delete(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.expenseType} - {self.nameOfRecipient}"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['beforeVAT', 'VATTotal', 'wth', 'net']
        else:
            return []
class Sales(models.Model):
    nameOfProject = models.CharField(max_length=200, verbose_name='Name of Client/Project')
    currencyType = models.ForeignKey(Currency, verbose_name='Currency', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_account = models.ForeignKey(Banks, on_delete=models.CASCADE, verbose_name='Credited Account')
    fsNumber = models.CharField(max_length=10,verbose_name='FS Number')
    RECIPIENT_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Company', 'Company'),
    ]
    recipientType = models.CharField(max_length=200, verbose_name='Recipient Type', choices=RECIPIENT_TYPE_CHOICES)
    remark = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Sales"

    def save(self, *args, **kwargs):
        # Credit the bank account
        self.bank_account.initial += self.amount
        self.bank_account.save()
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        # Rollback bank account transaction
        self.bank_account.initial -= self.amount
        self.bank_account.save()
        super().delete(*args, **kwargs)