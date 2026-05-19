from django.db import models

# --- CATEGORY MODEL ---
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self): 
        return self.name


# --- PRODUCT MODEL ---
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=10)
    description = models.TextField(blank=True)
    
    # Hybrid Toggles for the Website
    is_customizable = models.BooleanField(default=False, help_text="Enable customization section?")
    show_font_picker = models.BooleanField(default=False, help_text="Show standard font options?")
    show_color_picker = models.BooleanField(default=False, help_text="Show standard color options?")
    
    def __str__(self): 
        return self.name

    @property
    def get_standard_fonts(self):
        """Hardcoded fonts for the aesthetic font-cards"""
        return {
            "'Playfair Display', serif": "Classic Serif",
            "'Dancing Script', cursive": "Elegant Script",
            "'Cinzel', serif": "Royal Cinzel",
            "'Sacramento', cursive": "Boho Sacramento",
            "'Bebas Neue', sans-serif": "Modern Bold",
            "'Lora', serif": "Poetry Italic"
        }

    @property
    def get_standard_colors(self):
        """Hardcoded colors for the palette swatches"""
        return {
            "Charcoal": "#3D3D3D",
            "Luxury Gold": "#D4AF37",
            "Rose Copper": "#B5838D",
            "Sage Green": "#8A9A5B",
            "Antique Silver": "#C0C0C0",
            "Terracotta": "#E2725B"
        }


# --- EXTRA CUSTOMIZATION (FOR SIZES, MATERIALS, ETC.) ---
class ExtraCustomization(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='extra_options')
    label = models.CharField(max_length=100, help_text="e.g. Select Size")
    values = models.CharField(max_length=500, help_text="Enter choices separated by commas: Small, Medium, Large")

    def get_values_list(self):
        """Splits comma-separated string into a list for the dropdown"""
        if self.values:
            return [x.strip() for x in self.values.split(',')]
        return []

    def __str__(self): 
        return f"{self.label} for {self.product.name}"


# --- IMPORTANT: CART & ORDER TRACKING ---
# Ensure your CartItem and OrderItem models have the 'custom_details' field
# If these models are in different apps (like 'cart' or 'orders'), 
# add this field to them there.

# Example for your CartItem (wherever it is defined):
# class CartItem(models.Model):
#     ...
#     custom_details = models.TextField(blank=True, null=True, help_text="Stores Font, Color, Size, etc.")