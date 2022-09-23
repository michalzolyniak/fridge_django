from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, \
    authenticate, logout
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Sum
from datetime import timedelta, datetime
from .forms import UserCreateForm, LoginForm, AddProductForm, \
    AddCategoryForm, AddProductToFridgeForm, AddNoteForm, RemoveProductFromFridgeForm
from .models import Fridge, Product, Category, Note

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
        fridge_data = Fridge.objects.filter(user_id=request.user.id, status__isnull=True).order_by('expiration_date')
        notes = Note.objects.filter(user_id=request.user.id)
        fridge_value = fridge_data.aggregate(Sum('purchase_price'))
        fridge_value = fridge_value['purchase_price__sum']
        waste_value = Fridge.objects.filter(user_id=request.user.id, status=2).aggregate(Sum('purchase_price'))
        waste_value = waste_value['purchase_price__sum']
        eaten_value = Fridge.objects.filter(user_id=request.user.id, status=1).aggregate(Sum('purchase_price'))
        eaten_value = eaten_value['purchase_price__sum']
        return render(request, "fridge/fridge.html",
                      {"fridge_data": fridge_data, "notes:": notes,
                       "fridge_value": fridge_value,
                       "waste_value": waste_value, "eaten_value": eaten_value})


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
            default_price = 1
            categories = cd['category']
            product = Product.objects.create(
                name=name,
                consumption_hours=consumption_hours,
                default_price=default_price
            )

            for category in categories:
                product.category.add(category)

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


class FridgeAddProductView(LoginRequiredMixin, View):
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


class NoteCreateView(LoginRequiredMixin, View):
    form_class = AddNoteForm

    def get(self, request, product_id, *args, **kwargs):
        form = self.form_class()
        product = Product.objects.get(id=product_id)
        context = {'form': form, 'product_name': product.name}
        return render(request, 'fridge/add_note.html', context)

    def post(self, request, product_id, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            note = cd['note']
            product = Product.objects.get(id=product_id)
            current_user = request.user
            Note.objects.create(
                product=product,
                user=current_user,
                notes=note
            )
            return redirect('fridge')
        return render(request, 'fridge/add_note.html', context)


class FridgeRemoveProductView(LoginRequiredMixin, View):
    form_class = RemoveProductFromFridgeForm

    def get(self, request, record_id, *args, **kwargs):
        form = self.form_class()
        fridge_data = Fridge.objects.get(id=record_id)
        context = {'form': form, 'product_name': fridge_data.product.name}
        return render(request, 'fridge/remove_product_fridge.html', context)

    def post(self, request, record_id, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            status = cd['status']
            fridge_data = Fridge.objects.get(id=record_id)
            if status == "3":
                fridge_data.delete()
            else:
                fridge_data.status = status  # change field
                fridge_data.status_date = datetime.now()  # change field
                fridge_data.save()  # this will update only
            return redirect('fridge')
        return render(request, 'fridge/add_note.html', context)


class FridgeWasteView(LoginRequiredMixin, View):
    def get(self, request):
        waste_data = Fridge.objects.filter(user_id=request.user.id, status=2).order_by('-status_date')
        waste_value = waste_data.aggregate(Sum('purchase_price'))
        waste_value = waste_value['purchase_price__sum']
        return render(request, "fridge/waste.html",
                      {"waste_data": waste_data, "waste_value": waste_value})


class FridgeEatenProductsView(LoginRequiredMixin, View):
    def get(self, request):
        eaten_data = Fridge.objects.filter(user_id=request.user.id, status=1).order_by('-status_date')
        eaten_value = eaten_data.aggregate(Sum('purchase_price'))
        eaten_value = eaten_value['purchase_price__sum']
        return render(request, "fridge/eaten_products.html",
                      {"eaten_data": eaten_data, "eaten_value": eaten_value})


class OpenProductView(LoginRequiredMixin, View):
    def get(self, request, record_id, *args, **kwargs):
        fridge_data = Fridge.objects.get(id=record_id)
        expiration_date = datetime.now() + timedelta(hours=fridge_data.product.consumption_hours)
        fridge_data.expiration_date = expiration_date  # change field
        fridge_data.open = True  # change field
        fridge_data.save()  # this will update only
        return redirect('fridge')


