from django.urls import path
from . import views 

app_name = 'shop'

urlpatterns = [
    path('shop/', views.categories, name='category_list'),
    path('shop/<slug:category_slug>', views.product_list ),
    path('shop/<slug:slug>/', views.product_detail, name='product_detail'),
]