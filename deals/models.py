"""This is the deals model

A basic deal should have:
Date, stock number, last name, first name, financed,
reserve, vsc, gap, tw, tricare, key, total profit, and manager.
"""

from django.db import models


# Create your models here.
class Deal(models.Model):

    MANAGER_CHOICES = [
        ("Victor", "Victor"),
        ("Kevin", "Kevin"),
        ("Paul", "Paul"),
    ]
    deal_date = models.DateField(auto_now_add=True)
    stock_number = models.CharField(max_length=8)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    financed = models.BooleanField(default=True)
    reserve = models.FloatField(default=0)
    vsc = models.FloatField(default=0)
    gap = models.FloatField(default=0)
    tw = models.FloatField(default=0)
    tricare = models.FloatField(default=0)
    key = models.FloatField(default=0)
    manager = models.CharField(max_length=20, choices=MANAGER_CHOICES, default="Victor")

    @property
    def total_profit(self):
        return self.reserve + self.vsc + self.gap + self.tw + self.tricare + self.key

    def __str__(self):
        return self.stock_number
