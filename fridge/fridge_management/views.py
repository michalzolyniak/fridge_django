from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, \
    authenticate, logout
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views import View
from datetime import timedelta, datetime
from .forms import UserCreateForm, LoginForm, AddProductForm, \
    AddCategoryForm, AddProductToFridgeForm, AddNoteForm, RemoveProductFromFridgeForm
from .models import Fridge, Product, Category, Note
from django.forms.models import model_to_dict

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
        fridge_data = Fridge.objects.filter(user_id=request.user.id, status__isnull=True).order_by('-expiration_date')
        note = Note.objects.filter(user_id=request.user.id)
        # for data in fridge_data:
        #     # print(data.name)
        #     # product = data.product
        #     product = Product.objects.filter(name=data.product.name)
        #     # product.category.all()
        #     breakpoint()
        # # categories = fridge_data.Category.all()
        # breakpoint()
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
            # categories = cd['category']
            category = cd['category']

            product = Product.objects.create(
                name=name,
                consumption_hours=consumption_hours,
                default_price=default_price
            )

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


# breakpoint()


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
