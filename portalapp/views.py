from django.shortcuts import render
from portalapp.models import Category, Expense
from portalapp.forms import ExpenseForm, CategoryForm


def start_page(request):
    all_categories = Category.objects.all()
    context = {'all_categories': all_categories}
    return render(request, 'base.html', context)


def show_all(request):
    all_expenses = Expense.objects.all()
    amount = sum([element.expense for element in all_expenses])
    context = {'all_expenses': all_expenses, 'amount': amount}
    return render(request, 'all_expenses.html', context)


def by_category(request, slug):
    category = Category.objects.get(slug=slug)
    expenses_by_category = Expense.objects.filter(category__slug=slug)
    amount = sum([element.expense for element in expenses_by_category])
    return render(request, 'by_category.html', {'all_expenses': expenses_by_category,
                                                'amount': amount,
                                                'category': category},
                  )


def add_expense(request):
    if request.method == "POST":
        expense_form = ExpenseForm(data=request.POST)
        if expense_form.is_valid():
            new_expense = expense_form.save()
            all_expenses = Expense.objects.filter(category__id=new_expense.category.id)
            amount = sum([element.expense for element in all_expenses])
            return render(request,
                          'success_add.html',
                          {'expense': new_expense,
                           'amount': amount})
    expense_form = ExpenseForm()
    return render(request, "new_exp.html", {"form": expense_form})


def add_category(request):
    if request.method == "POST":
        category_form = CategoryForm(data=request.POST)
        if category_form.is_valid():
            new_category = category_form.save(commit=False)
            new_category.slug = new_category.name.replace(' ', '')
            new_category.save()
            return render(request,
                          'success_add_cat.html',
                          {'category': new_category})
    category_form = CategoryForm()
    return render(request, "new_cat.html", {"form": category_form})
