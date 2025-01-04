from django.shortcuts import render, redirect, get_object_or_404
from .models import Budget, Transaction
from .forms import TransactionForm, GoalForm

def home(request):
    budget = Budget.objects.first()
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GoalForm(instance=budget)
    
    money_left = None
    if budget and budget.goal_amount:
        money_left = budget.goal_amount - budget.total_spent
    
    transactions = Transaction.objects.all()
    return render(request, 'exp/home.html', {'budget': budget, 'form': form, 'money_left': money_left, 'transactions': transactions})

def add_transaction(request):
    budget = Budget.objects.first()
    if not budget:
        budget = Budget.objects.create(user="Default User")
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.budget = budget
            transaction.save()
            budget.total_spent += transaction.amount
            budget.save()
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'exp/add_transaction.html', {'form': form})

def history(request):
    transactions = Transaction.objects.all()
    return render(request, 'exp/history.html', {'transactions': transactions})

def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    budget = transaction.budget  # Get the associated budget from the transaction

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        previous_amount = transaction.amount
        if form.is_valid():
            updated_transaction = form.save(commit=False)
            updated_transaction.save()
            
            # Adjust total_spent: subtract previous amount and add the updated amount
            budget.total_spent += updated_transaction.amount - previous_amount
            budget.save()
            
            return redirect('history')  # Redirect to transaction history page
        else:
            print(form.errors)  # Debugging: Print form errors if the form is invalid
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'exp/update_transaction.html', {'form': form})

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    budget = transaction.budget  # Get the associated budget from the transaction
    budget.total_spent -= transaction.amount  # Adjust the total_spent
    budget.save()
    transaction.delete()
    return redirect('history')

def clear_budget(request):
    if request.method == 'POST':
        budget = Budget.objects.first()
        if budget:
            Transaction.objects.filter(budget=budget).delete()
            budget.total_spent = 0
            budget.save()
        return redirect('home')
    return render(request, 'exp/clear_budget.html')