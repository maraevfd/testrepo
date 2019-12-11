from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, render_to_response
from portalapp.models import Category, Expense, Salary
from portalapp.forms import ExpenseForm, CategoryForm, SalaryForm, SendEmailForm
from django.core.mail import send_mail


def get_income():
    all_expenses = Expense.objects.all()
    all_salaries = Salary.objects.all()
    income = sum([element.amount for element in all_salaries]) - sum(
                [element.expense for element in all_expenses])
    return income


def start_page(request):
    all_categories = Category.objects.all()
    salaries = Salary.objects.all()
    income = get_income()
    context = {'all_categories': all_categories,
               'salaries': salaries,
               'income': income}
    return render(request, 'base.html', context)


def get_a_salary(request):
    if request.method == "POST":
        salary_form = SalaryForm(data=request.POST)
        if salary_form.is_valid():
            new_salary = salary_form.save()
            income = get_income()
            return render(request,
                          'success_add_salary.html',
                          {'new_salary': new_salary,
                           'income': income})
    salary_form = SalaryForm()
    return render(request, "new_salary.html", {"form": salary_form})


def show_all(request):
    all_expenses = Expense.objects.all()
    paginator = Paginator(all_expenses, 5)
    page = request.GET.get('page')
    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        expenses = paginator.page(1)
    except EmptyPage:
        expenses = paginator.page(paginator.num_pages)
    amount = sum([element.expense for element in all_expenses])
    context = {'expenses': expenses, 'amount': amount}
    return render_to_response('all_expenses.html', context)


def by_category(request, slug):
    category = Category.objects.get(slug=slug)
    exp_by_catg = Expense.objects.filter(category__slug=slug)
    amount = sum([element.expense for element in exp_by_catg])
    return render(request, 'by_category.html', {'all_expenses': exp_by_catg,
                                                'amount': amount,
                                                'category': category,})


def add_expense(request):
    if request.method == "POST":
        expense_form = ExpenseForm(data=request.POST)
        if expense_form.is_valid():
            new_expense = expense_form.save()
            all_expenses = Expense.objects.filter(
                category__id=new_expense.category.id)
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
                message += '{} {} purchased. Spent {} rubles\n'.format(
                    expense.date,
                    expense,
                    expense.expense)
            message += "Open category {} \n\nAdded comment: {}".format(
                obj_url,
                cd['comment'])
            send_mail(subject,
                      message,
                      'admin@mycost_accounting.com',
                      [cd['address']])
            sent = True
    else:
        form = SendEmailForm()
    return render(request, 'send.html', {'category': obj,
                                         'form': form,
                                         'sent': sent})
