from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'avaliable', 'created', 'updated']
    list_filter = ['category', 'avaliable', 'created', 'updated']
    list_editable = ['price', 'avaliable']
    prepopulated_fields = {'slug': ('name',)}
