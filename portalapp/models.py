from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField()
    limit = models.DecimalField(default=100,
                                max_digits=10,
                                decimal_places=2)

    def get_absolute_url(self):
        return reverse('by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Expense(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    expense = models.DecimalField(validators=[MinValueValidator(0.01)],
                                  error_messages={'min_value': 'Invalid payment amount'},
                                  max_digits=10,
                                  decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date',)

