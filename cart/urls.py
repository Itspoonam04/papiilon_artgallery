from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_cart'),
    path('update/<int:id>/', views.update_quantity, name='update_cart'),
]