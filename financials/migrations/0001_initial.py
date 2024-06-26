# Generated by Django 4.2.9 on 2024-04-09 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankName', models.CharField(max_length=100, verbose_name='Name of Bank')),
                ('initial', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Banks',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currencySymbol', models.CharField(max_length=10, verbose_name='Currency Code')),
                ('currencyName', models.CharField(max_length=100, verbose_name='Currency Name')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenseName', models.CharField(max_length=100, verbose_name='Expense Name')),
                ('description', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Expense Types',
            },
        ),
        migrations.CreateModel(
            name='TaxType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vatName', models.CharField(max_length=200, verbose_name='Tax Name')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Rate(%)')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Tax Types',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameOfProject', models.CharField(max_length=200, verbose_name='Name of Client/Project')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fsNumber', models.CharField(max_length=10, verbose_name='FS Number')),
                ('recipientType', models.CharField(choices=[('Individual', 'Individual'), ('Company', 'Company')], max_length=200, verbose_name='Recipient Type')),
                ('remark', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.banks', verbose_name='Credited Account')),
                ('currencyType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.currency', verbose_name='Currency')),
            ],
            options={
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameOfRecipient', models.CharField(max_length=200, verbose_name='Recipient Name')),
                ('totalAmount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Amount')),
                ('beforeVAT', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Before VAT')),
                ('VATTotal', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='VAT Total')),
                ('wth', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='WTH')),
                ('net', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Net')),
                ('fsNO', models.CharField(max_length=10, verbose_name='FS No')),
                ('recipientType', models.CharField(choices=[('Individual', 'Individual'), ('Company', 'Company')], max_length=200, verbose_name='Recipient Type')),
                ('projectName', models.CharField(max_length=200, verbose_name='Project Name')),
                ('remark', models.TextField(verbose_name='Remark')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.banks', verbose_name='Debited Account')),
                ('expenseType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.expensetype', verbose_name='Expense Type')),
                ('vatType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_vat', to='financials.taxtype', verbose_name='VAT Type')),
                ('wthType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_wth', to='financials.taxtype', verbose_name='WTH Type')),
            ],
            options={
                'verbose_name_plural': 'Expenses',
            },
        ),
        migrations.AddField(
            model_name='banks',
            name='currencyType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.currency', verbose_name='Currency'),
        ),
    ]
