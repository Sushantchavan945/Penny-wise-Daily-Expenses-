from django.db import models

# Create your models here.
class Transactions(models.Model):
    choices_1=(('Income','Income'),('Expense','Expense'))
    choices_2=(('Bills','Bills'),('Food','Food'),('Clothes','Clothes'),('Medical','Medical'),('Housing','Housing'),('Salary','Salary'),('Social','Social'),('Transport','Transport'),('Vacation','Vacation'),('Random','Random'))

    transactions_type=models.CharField(max_length=100,choices=choices_1)
    amount=models.FloatField()
    transaction_date=models.DateField()
    category=models.CharField(max_length=100,choices=choices_2)
    description=models.TextField()


    def save(self,*args,**kwargs):
        if self.transactions_type=='Income' and self.category not in ['Salary','Social','Random']:
            raise ValueError("Income Transactions can only have 'salary','Social' or, 'random'.")
        super().save(*args,**kwargs)

    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name="Transaction"
        verbose_name_plural="Transactions"
        ordering=["-transaction_date"]

