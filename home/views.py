from django.shortcuts import render,redirect
from django.db.models import Sum
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from .models import *
import csv
from .models import *
from .main import *
# Create your views here.
def index(request):
    transactions=Transactions.objects.all()
    total_income=Transactions.objects.filter(transactions_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses=Transactions.objects.filter(transactions_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_income=total_income-total_expenses

    filter_type = None
    filter_date_from = None
    filter_date_to = None
    filter_category = []

    if request.method=='POST':
        filter_type=request.POST.get('type')
        filter_date_from=request.POST.get('date_from')
        filter_date_to=request.POST.get('date_to')
        filter_category=request.POST.getlist('category')
  
        filters=Q()
        if filter_type and filter_type!='Any' :
            filters &= Q(transactions_type=filter_type)
        if filter_date_from:
            filters &= Q(transaction_date__gte=filter_date_from)
        if filter_date_to:
            filters &= Q(transaction_date__lte=filter_date_to)
        if filter_category:
            filters &= Q(category__in=filter_category)
        transactions = Transactions.objects.filter(filters)
    context={
        'transactions':transactions,
        'total_income':total_income,
        'total_expense':total_expenses,
        'net_income':net_income,
        'filter_type':filter_type,
        'filter_date_from':filter_date_from,
        'filter_date_to':filter_date_to,
        'filter_category':filter_category

    }
    return render(request,'index.html',context)

def add_trans(request):
    if request.method=='POST':
        transaction_type=request.POST.get('type')
        amount=request.POST.get('amount')
        transaction_date=request.POST.get('date')
        transaction_category=request.POST.get('category')
        description=request.POST.get('description')

        Transactions.objects.create(transactions_type=transaction_type,amount=amount,transaction_date=transaction_date,category=transaction_category,description=description)
        return redirect('index')
    return render(request,'add_trans.html')

def chart_js(request):
    #For Bar chart (Income Vs Expense)
    categories = ['Income','Expense']
    income=Transactions.objects.filter(transactions_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense=Transactions.objects.filter(transactions_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    income_ = [income]
    expense_ = [expense]

    #For pie chart (categories)
    categories_expense=Transactions.objects.values('category').annotate(total_expense=Sum('amount'))
    categories_pie=[entry['category'] for entry in categories_expense]
    total_expenses_pie=[entry['total_expense'] for entry in categories_expense]
    print(categories_expense)
    context = {
        'categories': categories,
        'income': income_,
        'expense': expense_,
        'categories_pie':categories_pie,
        'total_expenses_pie':total_expenses_pie
    }
    return render(request,'chart.html',context)

def delete_trans(request,id):
    transaction=Transactions.objects.get(id=id)
    transaction.delete()
    messages.success(request,'Deleted successfully')
    return redirect('index')

def download_expense(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write header row
    writer.writerow(['Date', 'Description', 'Category', 'Amount'])  # Add relevant fields

    # Write data rows
    expenses = Transactions.objects.all()  # Adjust queryset if needed
    for expense in expenses:
        writer.writerow([expense.transaction_date.strftime('%Y-%m-%d'),expense.category, expense.description, expense.category, expense.amount])
    return response

def insights(request):
    user_query=""
    response=""
    
    if request.method=='POST':
        user_query=request.POST.get('query')
        response = analyze_expenses(user_query)
    
    return render(request,'assistant.html',context={'ai_response':response})
