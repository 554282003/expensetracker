from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse 
from userprefrences.models import UserPreference
# Create your views here.

def search_expense(request):
    if request.method == 'GET':
        print("hi")
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchfield')
        expense = Expense.objects.filter(
            amount__startswith=search_str,owner=request.user) | Expense.objects.filter(
            date__startswith=search_str,owner=request.user) | Expense.objects.filter(
            description__icontains=search_str,owner=request.user) | Expense.objects.filter(
            category__icontains=search_str,owner=request.user)

        data = expense.values()
        return JsonResponse(list(data),safe=False)

@login_required(login_url='/authentication/login')
def HomeView(request):
    expense = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expense,2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    print(page_obj,"page")
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses':expense,
        'page_obj':page_obj,
        'currency': currency
    }
    # print(user_exp)
    return render(request,'expenses/index.html',context)
@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'value':request.POST
    }
    if request.method != 'POST':
        return render(request,'expenses/add_expense.html',context)
    
    amount = request.POST.get('amount')
    description = request.POST.get('description')
    date = request.POST['date']
    category = request.POST['category']

    required_fields = ['amount', 'description', 'date', 'category']
    for field in required_fields:
        if not request.POST.get(field):
            messages.error(request, f'{field.capitalize()} is required.')
            return render(request, 'expenses/add_expense.html', context)
    Expense.objects.create(owner=request.user,amount=amount,date=date,category=category,description=description)
    messages.success(request,'Expense is created successfully')

    return redirect('home')


def expense_edit(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'value':expense,
        'categories':categories
    }
    if request.method == "GET":
        return render(request,'expenses/expense-edit.html',context)
    else:
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST['date']
        category = request.POST['category']

        required_fields = ['amount', 'description', 'date', 'category']
        for field in required_fields:
            if not request.POST.get(field):
                messages.error(request, f'{field.capitalize()} is required.')
                return render(request, 'expenses/expense-edit.html', context)
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()
        messages.success(request,'Expense is update successfully')

        return redirect('home') 
        
def expense_delete(request,id):
    print(id)
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,'Expense is removed')
    return redirect('home')