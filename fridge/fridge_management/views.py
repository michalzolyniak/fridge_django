from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, \
    authenticate, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView, ListView, RedirectView
from django.views.generic import FormView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.views import View
from .forms import UserCreateForm, LoginForm, AddProductForm, AddCategoryForm
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
        fridge_data = Fridge.objects.all().order_by('date_added')
        # fridge_data = Fridge.objects.filter(User).order_by('date_added')
        return render(request, "fridge/fridge.html",
                      {"fridge_data": fridge_data})


# class ProductCreateView(CreateView):
#     model = Product
#     template_name = 'fridge/add_product.html'
#     fields = ['name', 'consumption_date_close', 'consumption_hours', 'category', 'default_price']
#
#     def get_success_url(self):
#         # breakpoint()
#         return reverse_lazy('fridge')

class ProductCreateView(View):
    form_class = AddProductForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'fridge/add_product.html', context)

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #
    #         first_name = cd['first_name']
    #         last_name = cd['last_name']
    #         school_class = cd['school_class']
    #         year_of_birth = cd['year_of_birth']
    #         student = Student.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             school_class=school_class,
    #             year_of_birth=year_of_birth
    #         )
    #         return redirect(f'/student/{student.pk}')


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
            # breakpoint()
            category = Category.objects.create(name=name)
            # return reverse_lazy('fridge')
            return redirect('/fridge/')
        return render(request, 'fridge/add_category.html', context)

            # return reverse_lazy('fridge')

