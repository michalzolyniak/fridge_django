"""fridge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fridge_management.views import \
    UserCreateView, LoginView, \
    LogoutView, FridgeView, ProductCreateView, \
    CategoryCreateView, FridgeAddProductView, NoteCreateView, FridgeRemoveProductView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_user/', UserCreateView.as_view(), name='add-user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', FridgeView.as_view(), name='fridge'),
    path('add_product/', ProductCreateView.as_view(), name='add-product'),
    path('add_category/', CategoryCreateView.as_view(), name='add-category'),
    path('add_product_to_fridge/', FridgeAddProductView.as_view(), name='add-fridge'),
    path('add_note_to_product/<int:product_id>/', NoteCreateView.as_view(), name='add-note'),
    path('remove_product_from_fridge/<int:record_id>/', FridgeRemoveProductView.as_view(), name='remove-fridge'),
]
