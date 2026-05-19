from reportlab.pdfgen import canvas
from django.http import HttpResponse


def generate_invoice(order):

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, "Art Gallery Invoice")

    p.drawString(100, 770, f"Order ID: {order.id}")

    p.drawString(100, 740, f"Customer: {order.user.username}")

    p.drawString(100, 710, f"Subtotal: ₹{order.subtotal}")

    p.drawString(100, 690, f"GST: ₹{order.gst}")

    p.drawString(100, 670, f"Total: ₹{order.total_amount}")

    p.drawString(100, 630, "Thank you for your purchase!")

    p.showPage()

    p.save()

    return response