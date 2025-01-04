from django import forms
from .models import Transaction, Budget

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['goal', 'goal_amount']
        labels = {
            'goal': 'Goal',
            'goal_amount': 'Goal Amount'
        }