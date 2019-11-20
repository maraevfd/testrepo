from django.db import models
from django.shortcuts import render, reverse


class Category(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField()
    total_expense = models.FloatField(default=0)
    limit = models.FloatField(default=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('people.views.details', args=[str(self.id)])


class Expense(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    expense = models.FloatField(default=0)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "Расходы в количестве {} руб. потрачено на категорию {}"\
            .format(self.expense, self.category.name)


