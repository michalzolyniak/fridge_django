from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Category, Product


STATUS_T0_CHOSE = (
    (1, "Eaten"),
    (2, "Ejected"),
    (3, "Cancel"),
)

User = get_user_model()


class UserCreateForm(forms.Form):
    login = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 != password2:
            raise ValidationError('Hasła nie są identyczne.')


class LoginForm(forms.Form):
    login = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        login = cd.get('login')
        password = cd.get('password')
        user = authenticate(username=login, password=password)
        if user is None:
            raise ValidationError('Dane logowania nie są prawidłowe')


class AddProductForm(forms.Form):
    name = forms.CharField()
    consumption_hours = forms.IntegerField()
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    # default_price = forms.DecimalField()


class AddCategoryForm(forms.Form):
    name = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exists():
            raise ValidationError('This Category already exist in our database.')
        return name


class AddProductToFridgeForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    purchase_price = forms.DecimalField()
    expiration_date = forms.DateField()
    date_added = forms.DateField(initial=datetime.now())
    open = forms.BooleanField(required=False)


class AddNoteForm(forms.Form):
    note = forms.CharField(widget=forms.Textarea)


class RemoveProductFromFridgeForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_T0_CHOSE)
