from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Product, Category, ExtraCustomization
from django.contrib.auth.forms import UserCreationForm
from wishlist.models import Wishlist
from cart.models import Cart, CartItem
from orders.models import Order

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    
    wishlist_item = False
    if request.user.is_authenticated:
        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()

    # These are passed to the template for the aesthetic swatches
    standard_colors = {
        "Charcoal": "#3D3D3D",
        "Gold": "#D4AF37",
        "Rose": "#B5838D",
        "Sage": "#8A9A5B",
        "Silver": "#C0C0C0"
    }

    return render(request, "product_detail.html", {
        "product": product,
        "wishlist_item": wishlist_item,
        "colors": standard_colors,
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'product_list.html', {
        'products': products,
        'category': category
    })

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    
    if not request.user.is_authenticated:
        return redirect('login') 

    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # 1. Capture the Mode
    purchase_mode = request.POST.get('purchase_mode', 'asis')
    customization_details = []

    if purchase_mode == 'custom':
        # 2. Capture Fixed Options (Text, Font, Color)
        font = request.POST.get('selected_font')
        color = request.POST.get('selected_color')
        text = request.POST.get('custom_text')
        
        if text: customization_details.append(f"Text: {text}")
        if font: customization_details.append(f"Font: {font}")
        if color: customization_details.append(f"Color: {color}")

        # 3. Capture Dynamic Extra Options (Size, Material, etc.)
        for key, value in request.POST.items():
            if key.startswith('extra_'):
                # Cleans the label name (e.g., extra_select-size -> Select Size)
                label = key.replace('extra_', '').replace('-', ' ').title()
                customization_details.append(f"{label}: {value}")

    # Combine all choices into one string for the Admin Panel
    final_specs = " | ".join(customization_details) if customization_details else "Standard (As Is)"

    # 4. Save to Cart
    # We use get_or_create including customizations so that different 
    # customizations of the same product stay as separate line items.
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        custom_details=final_specs # Make sure this field exists in your CartItem model
    )

    if not item_created:
        cart_item.quantity += 1
    
    cart_item.save()

    return redirect('/cart/')

def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_customers = User.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    recent_orders = Order.objects.order_by('-created_at')[:5]
    low_stock_products = Product.objects.filter(stock__lt=5)

    context = {
        "total_orders": total_orders,
        "total_products": total_products,
        "total_customers": total_customers,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
        "low_stock_products": low_stock_products,
    }
    return render(request, "admin_dashboard.html", context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})