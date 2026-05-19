from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from decimal import Decimal
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from cart.models import CartItem
from .models import Order, OrderItem, Coupon

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "my_orders.html", {"orders": orders})

@login_required
def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    return render(request, "order_detail.html", {"order": order})

@login_required
def checkout(request):
    items = CartItem.objects.filter(cart__user=request.user)
    
    if not items.exists():
        return redirect('home')

    

    subtotal = Decimal("0")
    for item in items:
        subtotal += item.product.price * item.quantity

    gst = subtotal * Decimal("0.18")
    discount = Decimal("0")
    coupon_code = ""

    # 1. APPLY COUPON LOGIC
    if request.method == "POST" and "apply_coupon" in request.POST:
        coupon_code = request.POST.get("coupon")
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            discount = (subtotal * Decimal(coupon.discount)) / Decimal("100")
        except Coupon.DoesNotExist:
            discount = Decimal("0")

    total = subtotal + gst - discount

    # 2. PLACE ORDER LOGIC
    if request.method == "POST" and "place_order" in request.POST:
        # Create the main Order
        new_order = Order.objects.create(
            user=request.user,
            subtotal=subtotal,
            gst=gst,
            total_amount=total
        )

        # Create OrderItems and Transfer Customizations
        for item in items:
            OrderItem.objects.create(
                order=new_order,
                product_name=item.product.name,
                price=item.product.price,
                # THIS IS THE KEY: Transfer the specs from Cart to Order
                custom_details=item.custom_details 
            )
            
            # Update Stock
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Clear the Cart
        items.delete()
        return redirect("my_orders") # Update this to your actual orders URL

    return render(request, "checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "gst": gst,
        "discount": discount,
        "total": total,
        "coupon_code": coupon_code
    })

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch





def generate_invoice(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Pappilon_Invoice_{order.id}.pdf"'

    # Create the canvas
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # --- BRAND HEADER ---
    p.setFillColor(colors.HexColor("#B5838D")) # Papillon Rose
    p.rect(0, height - 100, width, 100, fill=1, stroke=0)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 60, "PAPILLON CREATIONS")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 80, "PREMIUM CUSTOM NAMEPLATES & HOME DECOR | PUNE")

    # --- ORDER INFO ---
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 140, "INVOICE TO:")
    
    p.setFont("Helvetica", 11)
    p.drawString(50, height - 160, f"Customer: {order.user.username.upper()}")
    p.drawString(50, height - 175, f"Email: {order.user.email}")
    
    # Right Side Info
    p.drawRightString(width - 50, height - 140, f"Invoice #: PPLN-{order.id}")
    p.drawRightString(width - 50, height - 160, f"Date: {order.created_at.strftime('%d %B, %Y')}")

    # --- TABLE HEADER ---
    y_position = height - 230
    p.setStrokeColor(colors.HexColor("#B5838D"))
    p.setLineWidth(1)
    p.line(50, y_position, width - 50, y_position)
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(55, y_position - 20, "DESCRIPTION")
    p.drawRightString(width - 55, y_position - 20, "AMOUNT")
    
    y_position -= 30

    # --- ITEMS LOOP ---
    for item in order.items.all():
        # Product Name
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50, y_position, item.product_name)
        p.drawRightString(width - 50, y_position, f"₹{item.price}")
        
        # Customization Details (The Aesthetic Part)
        if item.custom_details:
            y_position -= 15
            p.setFont("Helvetica-Oblique", 9)
            p.setFillColor(colors.HexColor("#6D6A75")) # Muted Sage/Gray
            
            # Splitting long detail strings so they don't overlap price
            detail_text = f"Personalization: {item.custom_details}"
            p.drawString(60, y_position, detail_text)
            p.setFillColor(colors.black)
            
        y_position -= 35
        
        # Page break check
        if y_position < 150:
            p.showPage()
            y_position = height - 50

    # --- TOTALS SECTION ---
    p.setDash(1, 2)
    p.line(350, y_position, width - 50, y_position)
    p.setDash()
    
    y_position -= 25
    p.setFont("Helvetica", 10)
    p.drawString(350, y_position, "Subtotal:")
    p.drawRightString(width - 50, y_position, f"₹{order.subtotal}")
    
    y_position -= 20
    p.drawString(350, y_position, "GST (18%):")
    p.drawRightString(width - 50, y_position, f"₹{order.gst}")
    
    y_position -= 30
    p.setFillColor(colors.HexColor("#B5838D"))
    p.rect(340, y_position - 10, 210, 30, fill=1, stroke=0)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(350, y_position, "TOTAL AMOUNT")
    p.drawRightString(width - 60, y_position, f"₹{order.total_amount}")

    # --- FOOTER ---
    p.setFillColor(colors.HexColor("#8D7B68"))
    p.setFont("Helvetica-Oblique", 9)
    p.drawCentredString(width/2, 60, "Every Papillon piece is handcrafted with love and signed by our artists.")
    p.drawCentredString(width/2, 45, "Thank you for supporting Pune's creative community!")
    
    p.showPage()
    p.save()
    return response