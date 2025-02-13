# Generated by Django 5.1.4 on 2024-12-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactions_type', models.CharField(choices=[('Income', 'Income'), ('Expense', 'Expense')], max_length=100)),
                ('amount', models.FloatField()),
                ('transaction_date', models.DateField()),
                ('category', models.CharField(choices=[('Bills', 'Bills'), ('Food', 'Food'), ('Clothes', 'Clothes'), ('Medical', 'Medical'), ('Housing', 'Housing'), ('Salary', 'Salary'), ('Social', 'Social'), ('Transport', 'Transport'), ('Vacation', 'Vacation'), ('Random', 'Random')], max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-transaction_date'],
            },
        ),
    ]
