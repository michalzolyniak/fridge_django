from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Category, Product

STATUS_T0_CHOSE = (
    (1, ""),
    (1.5, "1+"),
)

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
    # categories = (Category.objects.values_list('id', 'name'))
    # choices = [(avatar.id, avatar_img(avatar, size)) for category in avatars]
    #category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    default_price = forms.DecimalField()


    # def clean_consumption_date_close(self):
    #     consumption_date_close = datetime.strptime(self.cleaned_data['consumption_date_close'], '%Y/%m/%d')
    #     print(consumption_date_close)
    #     if not isinstance(consumption_date_close, datetime):
    #         raise ValidationError('Consumption date close must be date in format YYYY-MM-DDDD')
    #     return consumption_date_close

    # def clean_consumption_hours(self):
    #     consumption_hours = self.cleaned_data['consumption_hours']
    #     if not isinstance(consumption_hours, int):
    #         raise ValidationError('Consumption hours close must be the whole number')
    #     return consumption_hours
    #
    # def clean_default_price(self):
    #     consumption_hours = self.cleaned_data['default_price']
    #     if not isinstance(consumption_hours, float):
    #         raise ValidationError('Default price close must be the float number')
    #     return consumption_hours


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
    date_added = forms.DateField()
    open = forms.BooleanField(required=False)


class AddNoteForm(forms.Form):
    note = forms.CharField(widget=forms.Textarea)


class RemoveProductFromFridgeForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_T0_CHOSE)


