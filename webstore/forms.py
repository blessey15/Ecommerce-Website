from django import forms

from .models import *

GENDER_CHOICES=(
    ('Male','Male'),
    ('Female','Female'),
)

class CustomerForms(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your name"}))
    contact = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your contact details"}))
    dob = forms.DateField(widget=forms.SelectDateWidget())
    gender = forms.ChoiceField( choices=GENDER_CHOICES,widget = forms.Select())

    class Meta:
        model=Customer
        fields=('name','contact','dob','gender')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        try:
            contact = int(contact)
        except ValueError:
            raise forms.ValidationError("The mobile number entered is not valid!!")
        return contact

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        return dob

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        return gender