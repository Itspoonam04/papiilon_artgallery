from .models import CartItem
from django.db.models import Sum

def cart_item_count(request):

    if request.user.is_authenticated:

        cart_count = CartItem.objects.filter(
            cart__user=request.user
        ).aggregate(total=Sum('quantity'))['total'] or 0

    else:
        cart_count = 0

    return {
        "cart_count": cart_count
    }