from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # path('',views.HomeView,name='home'),
    path('',views.index,name='income'),
    path('add-income/',views.add_income,name='add-income'),
    path('income-edit/<int:id>',views.edit_income,name='income-edit'),
    path('income-delete/<int:id>',views.delete_income,name='income-delete'),
    path('search-income',csrf_exempt(views.search_income),name='search-income'),
]
