from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Views
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
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# from django.contrib.auth import authenticate
# from django.contrib.auth import login, logout
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
#
# from ecommerce.decorators import *
# from .forms import *
#
#
# @unauthenticated_user
# def registration_view(request):  # Function used for registration
#     context = {}
#     if request.POST:
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             print('hello')
#             form.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             registration = authenticate(email=email, password=raw_password)
#             login(request, registration)
#             return redirect('store')
#         else:
#             context['registration_form'] = form
#     else:
#         form = RegistrationForm()
#         context['registration_form'] = form
#     return render(request, 'registration/register.html', context)
#
#
# @unauthenticated_user
# def login_view(request):  # Function used for login
#     context = {}
#     user = request.user
#
#     if request.POST:
#         form = AccountAuthenticationForm(request.POST)
#         print('hello..')
#
#         if form.is_valid():
#             print('hellon')
#             email = request.POST['email']
#             password = request.POST['password']
#             user = authenticate(email=email, password=password)
#
#         if user:
#             login(request, user)
#             return redirect('store')
#
#     else:
#         form = AccountAuthenticationForm()
#
#     context['login_form'] = form
#     return render(request, 'registration/login.html', context)
#
#
# @login_required(login_url='login')
# def logout_view(request):  # Function to logout
#     logout(request)
#     return redirect('store')
#
#
# @login_required(login_url='login')  # to update username and email
# def account_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#
#     context = {}
#
#     if request.POST:
#         form = AccountUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect("home")
#
#     else:
#         form = AccountUpdateForm(
#             initial={
#                 'email': request.user.email,
#                 'username': request.user.username,
#             }
#         )
#     context['account_form'] = form
#     return render(request, 'account.html', context)
# def feedback_view(request):
#         return render(request, 'feedback.html', {})
#