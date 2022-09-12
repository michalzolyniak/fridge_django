from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, \
    authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView, ListView, RedirectView
from django.views.generic import FormView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.views import View
from .forms import UserCreateForm, LoginForm, AddProductForm, \
    AddCategoryForm, AddProductToFridgeForm
from .models import Fridge, Product, Category

User = get_user_model()


class UserCreateView(FormView):
    template_name = 'fridge/user_create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        User.objects.create_user(
            username=cd['login'],
            password=cd['password1'],
            email=cd['email'],
        )
        return response


class LoginView(FormView):
    template_name = 'fridge/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('fridge')

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['login'], password=cd['password'])
        login(self.request, user)
        return response


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class FridgeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            fridge_data = Fridge.objects.filter(user_id=request.user.id).order_by('date_added')
            return render(request, "fridge/fridge.html",
                          {"fridge_data": fridge_data})
        else:
            return redirect('login')


class ProductCreateView(View):
    form_class = AddProductForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'fridge/add_product.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            consumption_date_close = cd['consumption_date_close']
            consumption_hours = cd['consumption_hours']
            default_price = cd['default_price']
            Product.objects.create(
                name=name,
                consumption_date_close=consumption_date_close,
                consumption_hours=consumption_hours,
                default_price=default_price
            )
            return redirect('fridge')
        return render(request, 'fridge/add_category.html', context)


class CategoryCreateView(View):
    form_class = AddCategoryForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'fridge/add_category.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            Category.objects.create(name=name)
            return redirect('fridge')
        return render(request, 'fridge/add_category.html', context)


# @login_required
class FridgeAddProductView(View):
    form_class = AddProductToFridgeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'fridge/add_product_fridge.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            current_user = request.user
            product = cd['product']
            purchase_price = cd['purchase_price']
            date_added = cd['date_added']
            is_open = cd['open']
            Fridge.objects.create(
                user=current_user,
                product=product,
                purchase_price=purchase_price,
                date_added=date_added,
                open=is_open
            )
            return redirect('fridge')
        return render(request, 'fridge/add_product_fridge.html', context)
# breakpoint()
