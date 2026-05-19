from django.urls import path
from . import views

urlpatterns = [

    path('my-orders/', views.my_orders, name='my_orders'),

    path('<int:id>/', views.order_detail, name='order_detail'),

    path('checkout/', views.checkout, name='checkout'),

    # CORRECT
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    

]