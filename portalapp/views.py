from django.shortcuts import render, get_object_or_404
from portalapp.models import Category, Expense
from portalapp.forms import ExpenseForm


def start_page(request):
    all_categories = Category.objects.all()
    context = {'all_categories': all_categories}
    return render(request, 'base.html', context)


def show_all(request):
    all_expenses = Expense.objects.all()
    amount = 0
    for expense in all_expenses:
        amount += expense.expense
    context = {'all_expenses': all_expenses, 'amount': amount}
    return render(request, 'all_expenses.html', context)


def by_category(request, slug):
    category = Category.objects.get(slug=slug)
    expenses_by_category = Expense.objects.filter(category__slug=slug)
    amount = 0
    for expense in expenses_by_category:
        amount += expense.expense
    return render(request, 'by_category.html', {'all_expenses': expenses_by_category,
                                                'amount': amount,
                                                'category': category},
                  )


def add_expense(request):
    if request.method == "POST":
        expense_form = ExpenseForm(data=request.POST)
        if expense_form.is_valid():
            new_expense = expense_form.save(commit=False)
            new_expense.save()
            all_expenses = Expense.objects.filter(category__id=new_expense.category.id)
            amount = 0
            for expense in all_expenses:
                amount += expense.expense
            return render(request,
                          'success_add.html',
                          {'expense': new_expense,
                           'amount': amount})
    expense_form = ExpenseForm()
    return render(request, "new_exp.html", {"form": expense_form})
