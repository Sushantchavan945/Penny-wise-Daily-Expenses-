from groq import Groq
from django.db.models import Sum
from django.conf import settings
from .models import *

def generate_transaction_summary():
    # Filtered for a specific user
    total_income = Transactions.objects.filter( transactions_type="Income").aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transactions.objects.filter( transactions_type="Expense").aggregate(Sum('amount'))['amount__sum'] or 0

    # Category-wise summary
    category_wise = Transactions.objects.filter().values('category').annotate(total=Sum('amount'))

    # Most recent transactions
    recent_transactions = list(
        Transactions.objects.filter().order_by('-transaction_date')[:5].values(
            'transactions_type', 'amount', 'transaction_date', 'category', 'description'
        )
    )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "category_wise": list(category_wise),
        "recent_transactions": recent_transactions,
    }

def analyze_expenses(user_input):
    transaction_summary = generate_transaction_summary()

    # Improved Prompt Structure
    prompt = f"""
You are a financial assistant. Below is the transaction summary for User:

- Total Income: {transaction_summary['total_income']}
- Total Expenses: {transaction_summary['total_expense']}
- Category-wise Breakdown: {transaction_summary['category_wise']}

Query: "{user_input}"

Provide a **precise response of exactly 35 words** addressing any suggestions or actions regarding the user's category-wise expenses or budgeting based on the input.
"""



    # Groq API Client
    client = Groq(api_key="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")

    completion = client.chat.completions.create(
        model="llama-3.2-1b-preview",
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.7,
    )
    return completion.choices[0].message.content
