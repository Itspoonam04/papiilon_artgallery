from django.shortcuts import render, redirect,get_object_or_404
from .models import Wishlist
from store.models import Product

def add_to_wishlist(request, id):

    product = Product.objects.get(id=id)

    Wishlist.objects.create(
        user=request.user,
        product=product
    )

    return redirect('/')

def wishlist_page(request):

    items = Wishlist.objects.filter(user=request.user)

    return render(request,'wishlist.html',{'items':items})

def toggle_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    item = Wishlist.objects.filter(
        user=request.user,
        product=product
    )

    if item.exists():
        item.delete()  # remove from wishlist
    else:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )

    return redirect(request.META.get('HTTP_REFERER'))