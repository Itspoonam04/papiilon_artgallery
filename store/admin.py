from django.contrib import admin
from .models import Category, Product, ExtraCustomization

class ExtraCustomizationInline(admin.TabularInline):
    model = ExtraCustomization
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_customizable', 'stock')
    list_filter = ('category', 'is_customizable')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ExtraCustomizationInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ExtraCustomization)