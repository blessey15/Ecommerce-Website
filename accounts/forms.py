from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Account


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username",
                                                             "class": "form-control form-control-user",
                                                             "id": "exampleInputUsername"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email",
                                                            "class": "form-control form-control-user",
                                                            "id": "exampleInputEmail"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password",
                                                                  "class": "form-control form-control-user",
                                                                  "id": "exampleInputPassword"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password",
                                                                  "class": "form-control form-control-user",
                                                                  "id": "exampleInputPassword"}))

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Enter Email Address",
                                                            "class": "form-control form-control-user",
                                                            "id": "exampleInputEmail"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password",
                                                                 "class": "form-control form-control-user",
                                                                 "id": "exampleInputPassword"}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login!")


class AccountUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username",
                                                             "class": "form-control form-control-user",
                                                             "id": "exampleInputUsername"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email Address",
                                                            "class": "form-control form-control-user",
                                                            "id": "exampleInputEmail"}))

    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" already in use' % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Email "%s" already in use' % username)