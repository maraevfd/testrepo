from django.shortcuts import render
from django.views import View
from portalapp.models import Category, Expense
from django.views.generic.list import ListView


class BaseView(View):

    template_name = 'base.html'

    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, self.template_name, context)


class ExpenseListView(ListView):

    template_name = 'all_expenses.html'
    model = Expense

    def get_context_data(self, *args, **kwargs):
        context = {'expenses': self.model.objects.all()}
        return context


def show_last(request):
    latest_expense_list = Expense.objects.order_by('date')[:1]
    context = {'latest_expense_list': latest_expense_list}
    return render(request, 'show_last.html', context)
