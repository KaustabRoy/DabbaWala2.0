from django.contrib import admin
from .models import User, Product, Category, SubCategory, Day, CartItem


# Configuring admin model view
class AdminUser(admin.ModelAdmin):
    list_display = ['email', 'name']

class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'descrption', 'items_img']

class AdminCategory(admin.ModelAdmin):
    list_display = ['id', 'cat_name']

class SubCategoryFeatures(admin.ModelAdmin):
    list_display = ['id', 'parent_cat', 'sub_cat_name']

class AdminCartItem(admin.ModelAdmin):
    list_display = ['user_email', 'selected_day', 'breakfast_items', 'lunch_items', 'dinner_items', 'order_id', 'order_date', 'order_time']


# Register your models here.

admin.site.register(User, AdminUser)
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(SubCategory, SubCategoryFeatures)
admin.site.register(Day)
admin.site.register(CartItem, AdminCartItem)
