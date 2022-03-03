from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

import json
import datetime

from .models import *
from .forms import CustomerForms
from .utils import cartData,cookieCart,guestOrder

@login_required
def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def home_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/index.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


def paypal(request):
    return render(request, 'payment.html', {})

@login_required
def home(request):
    return render(request, "registration/success.html", {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def customer_profile(request):
    context = {}
    # try:
    #     post = request.user.post
    # except Customer.DoesNotExist:
    #     post = Customer(user=request.user)
    if request.method == "POST":
        print('hello')
        form = CustomerForms(data=request.POST, instance=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            name = form.cleaned_data.get('name')
            contact = form.cleaned_data.get('contact')
            dob = form.cleaned_data.get('dob')
            gender = form.cleaned_data.get('gender')
            customer = Customer.objects.create(
                user=request.user,
                name = name,
                contact = contact,
                gender = gender,
            )
            # customer.name = name
            customer.save()
            return redirect('store')
    else:
        form = CustomerForms(instance=request.user)
        context['form'] = form
    # else:
    #     form = CustomerForms(
    #         initial={
    #             'name': post.name,
    #             'contact': post.contact,
    #             'dob': post.dob,
    #             'gender': post.gender,})
    return render(request, 'store/profilecreate.html', context)

