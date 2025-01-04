from django.db import models

# Create your models here.
class Budget(models.Model):
    user = models.CharField(max_length=100)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    goal = models.CharField(max_length=200, blank=True, null=True)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

class Transaction(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

