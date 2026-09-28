from django.db import models

class Account(models.Model):
    """Kassa / Hisob raamlar"""
    CURRENCY_CHOICES = (
        ('UZS', 'So\'m'),
        ('USD', 'Dollar'),
    )
    name = models.CharField(max_length=100) # Masalan: Asosiy Kassa UZS, Naqd USD
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UZS')

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency})"

class Transaction(models.Model):
    """Moliyaviy operatsiyalar (Kirim / Chiqim)"""
    TYPE_CHOICES = (
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} ({self.account.name})"