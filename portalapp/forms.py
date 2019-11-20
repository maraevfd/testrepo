from django import forms


class AddCategory(forms.Form):
    name = forms.CharField(max_length=140)
    slug = forms.SlugField()
    total_expense = forms.FloatField(default=0)
    limit = forms.FloatField(default=100)
