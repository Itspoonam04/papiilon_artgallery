from django.urls import path
from . import views

urlpatterns = [

    path('', views.wishlist_page, name='wishlist'),

    path('add/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('toggle/<int:product_id>/', views.toggle_wishlist, name="toggle_wishlist"),

]