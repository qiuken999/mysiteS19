from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

# Create your views here.
# Import necessary classes
from django.http import HttpResponse

from myapp.forms import OrderForm, InterestForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
# Create your views here.

#global variable declare and use the 'global' in the def
#Upper Capital is better
about_visits = 0

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list})

# def about(request):
#    response = HttpResponse()
#    heading1 = '<p>' + 'This is an Online Store APP.'+ '</p>'
#    response.write(heading1)
#    return response

def about(request):
    global about_visits
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        about_visits += 1
        #expired after 5 mins
        request.session.set_expiry(5^60)
    #set and test should be in different view
    request.session.set_test_cookie()
    return render(request,'myapp/about.html', {"about_visits":about_visits})

# def detail(request, cat_no):
#     # try:
#     #     a = Category.objects.get(id=cat_no)
#     # except Category.DoesNotExist:
#     #     raise Http404("Category does not exist!")
#     # return render(request, 'myapp/detail.html', {'detail':a})
#
#     outcome = get_object_or_404(Category, pk=cat_no)
#     cat = Category.objects.get(id=cat_no)   #cat is the chosen Category object
#     response = HttpResponse()
#     para1 = '<p>' + 'Location: ' + cat.warehouse + '</p>'
#     response.write(para1)
#
#     categoryName = cat.name
#
#     pro = Product.objects.filter(category__name=categoryName)    #pro has 4 dic paris
#     for p in pro:
#         para = '<p>' + 'products: ' + p.name + '</p>'
#         response.write(para)
#     return response
#     #return render(request, 'myapp/outcome.html', {'outcome': outcome})

def detail(request, cat_no):
    object = get_object_or_404(Category, pk=cat_no)
    cat = Category.objects.get(id=cat_no)
    list=cat.products.all()
    return render(request, 'myapp/detail.html', {'category': cat,'list':list})

def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})

def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form':form, 'msg':msg, 'prodlist':prodlist})

def productdetail(request, prod_id):
    item=Product.objects.get(id=prod_id)
    if request.method == 'GET':
        form = InterestForm(request.GET)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        print(form.is_valid())
        print(form.cleaned_data['interested'])
        if form.is_valid():
            if form.cleaned_data['interested'] == "1":
                print("ok")
                item.interested=item.interested + 1
                item.save()
            # return render(request, 'myapp/index.html')

    return render(request, 'myapp/productdetail.html', {'form': form, 'item': item})

#Lab7 login
#username=mary
#pwd=Mary12345
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                #generate date&time
                #store it into last_login
                now = datetime.datetime.now()
                lastlogin = now.strftime("%m/%d/%Y, %H:%M:%S")
                # lastlogin = user.last_login
                #set item
                request.session['username'] = username
                #index page visited, if last_login exists in session
                #if not exist, show msg. else show last_login value
                if not request.session.has_key('last_login'):
                    lastlogin = 'Your last login was more than one hour ago'
                    request.session['last_login'] = lastlogin
                    print(lastlogin)
                    # return redirect('/myapp/index')
                    return redirect('/myapp/myorders')
                    # return render(request, 'myapp/index.html', {'lastlogin': lastlogin})
                else:
                    request.session['last_login'] = lastlogin
                    request.session.set_expiry(3600)
                    print(lastlogin)
                    return redirect('/myapp/myorders')
                    # return redirect('/myapp/index')
                    # return render(request, 'myapp/index.html', {'lastlogin': lastlogin})
                # request.session.set_expiry(60 ^ 60)
                # return HttpResponseRedirect(reverse(myorders))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    # return HttpResponseRedirect(reverse(index))
    return HttpResponseRedirect('/myapp/index')

def myorders(request):
    msgNotUser = 'You are not a registered client!'
    msgNotOrder = 'This account does not have an order yet.'
    if request.user.is_authenticated:
        if (Order.objects.filter(client=request.user).exists() == True):
            orderlist = Order.objects.get(client=request.user)
            # orderlist = Order.objects.all()
            return render(request, 'myapp/myorders.html', {'orderlist': orderlist})
        else:
            return render(request, 'myapp/myorders.html', {'msgNotOrder': msgNotOrder})
    else:
        return render(request, 'myapp/myorders.html', {'msgNotUser': msgNotUser})

#username = try
#pwd = Trytry123
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('passwordA')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/myapp/index')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})


