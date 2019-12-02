from _decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField()
    total_expense = models.FloatField(default=0)
    limit = models.FloatField(default=100)

    def get_absolute_url(self):
        return reverse('by_category',
                       args=[self.slug])

    def __str__(self):
        return self.name


class Expense(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    expense = models.FloatField(default=0, validators=[MinValueValidator(Decimal('0.001'))])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date',)

