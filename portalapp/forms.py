from django import forms
from .models import Expense, Category, Salary


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('category', 'title', 'expense')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ('amount',)


class SendEmailForm(forms.Form):
    address = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)
