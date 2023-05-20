from django.contrib import admin
from .models import Category, FoodItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}
    list_display = ('category_name', 'vendor')
    search_fields = ('category_name', 'vendor__vendor_name')


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_tittle', )}
    list_display = ('food_tittle', 'category', 'vendor','price','is_available')
    search_fields = ('food_tittle', 'category__category_name', 'vendor__vendor_name','price')
    list_filter = ('is_available', )




admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
