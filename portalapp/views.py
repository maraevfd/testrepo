from django.shortcuts import render, get_object_or_404
from portalapp.models import Category, Expense
from portalapp.forms import ExpenseForm, CategoryForm, SendEmailForm
from django.core.mail import send_mail


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
    exceeded = False
    difference = category.limit - amount
    if amount > category.limit:
        exceeded = True
        difference = -difference
    return render(request, 'by_category.html', {'all_expenses': expenses_by_category,
                                                'amount': amount,
                                                'category': category,
                                                'exceeded': exceeded,
                                                'difference': difference})


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


def send_email(request, category_id):
    obj = get_object_or_404(Category, id=category_id)
    expenses = Expense.objects.filter(category__id=category_id)
    sent = False
    if request.method == "POST":
        form = SendEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj_url = request.build_absolute_uri(obj.get_absolute_url())
            subject = "This is a report by category {}".format(obj.name)
            message = ''
            for expense in expenses:
                message += '{} {} purchased. Spent {} rubles\n'.format(expense.date,
                                                                       expense,
                                                                       expense.expense)
            message += "Open category {} \n\nAdded comment: {}".format(obj_url,
                                                                       cd['comment'])
            send_mail(subject, message, 'admin@mycost_accounting.com', [cd['address']])
            sent = True
    else:
        form = SendEmailForm()
    return render(request, 'send.html', {'category': obj,
                                         'form': form,
                                         'sent': sent})
