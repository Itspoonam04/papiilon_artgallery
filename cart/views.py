from django.shortcuts import render
from .models import CartItem
from decimal import Decimal

def cart_view(request):

    items = CartItem.objects.filter(cart__user=request.user)

    subtotal = Decimal("0")

    for item in items:
        subtotal += item.product.price * item.quantity

    return render(request, "cart.html", {
        "items": items,
        "subtotal": subtotal
    })

from django.shortcuts import get_object_or_404, redirect

def remove_from_cart(request, item_id):
    # This assumes 'CartItem' is your model name
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart') # Redirect back to the cart page

from django.shortcuts import redirect

def remove_from_cart(request, id):

    item = CartItem.objects.get(id=id)

    item.delete()

    return redirect('/cart/')

def update_quantity(request, id):

    item = CartItem.objects.get(id=id)

    action = request.GET.get('action')

    if action == "increase":
        item.quantity += 1

    elif action == "decrease":

        if item.quantity > 1:
            item.quantity -= 1

    item.save()

    return redirect('/cart/')