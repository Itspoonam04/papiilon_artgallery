from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # REFINED CUSTOMIZATION FIELDS
    # This single field will store the combined string from views.py 
    # e.g., "Text: Poonam | Font: Elegant | Color: Gold | Size: Large"
    custom_details = models.TextField(null=True, blank=True)

    # Keep these if you want to store them separately, 
    # but 'custom_details' is better for the dynamic Hybrid system.
    custom_name = models.CharField(max_length=200, null=True, blank=True)
    font = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        # This makes the customization visible in the Admin list view
        if self.custom_details:
            return f"{self.product.name} ({self.custom_details})"
        return self.product.name