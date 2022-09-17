from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, \
    authenticate, logout
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views import View
from datetime import timedelta
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


class FridgeView(LoginRequiredMixin, View):
    def get(self, request):
        expire_date = {}
        fridge_data = Fridge.objects.filter(user_id=request.user.id).order_by('-expiration_date')
        return render(request, "fridge/fridge.html",
                      {"fridge_data": fridge_data, "expire_date": expire_date})


class ProductCreateView(LoginRequiredMixin, View):
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
                consumption_hours = cd['consumption_hours']
                default_price = cd['default_price']
                Product.objects.create(
                    name=name,
                    consumption_hours=consumption_hours,
                    default_price=default_price
                )
                return redirect('fridge')
            return render(request, 'fridge/add_category.html', context)


class CategoryCreateView(LoginRequiredMixin, View):
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


class FridgeAddProductView(LoginRequiredMixin,View):
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
            expiration_date = cd['expiration_date']
            product_data = Product.objects.get(name=product)
            if is_open:
                expiration_date = date_added + timedelta(hours=product_data.consumption_hours)
            Fridge.objects.create(
                user=current_user,
                product=product,
                purchase_price=purchase_price,
                date_added=date_added,
                open=is_open,
                expiration_date=expiration_date
            )
            return redirect('fridge')
        return render(request, 'fridge/add_product_fridge.html', context)
# breakpoint()
