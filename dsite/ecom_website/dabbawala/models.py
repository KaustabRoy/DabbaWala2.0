from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(blank = True, null = True, unique=True)
    name = models.CharField(max_length = 100, blank = True, null = True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []


class Category(models.Model):
    cat_name = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.cat_name
    
class SubCategory(models.Model):
    parent_cat = models.ForeignKey(Category, null = True, on_delete = models.CASCADE)
    sub_cat_name = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.sub_cat_name

class Product(models.Model):
    title = models.CharField(max_length = 100, null = True)
    price = models.CharField(max_length = 10, null = True)
    descrption = models.CharField(max_length = 1000, null = True)
    item_cat = models.ForeignKey(Category, null = True, on_delete = models.CASCADE)
    # item_sub_cat = models.ManyToManyField(SubCategory)
    items_img = models.ImageField(upload_to = 'food_items')

class Day(models.Model):
    day_name = models.CharField(max_length = 20)

    def __str__(self) -> str:
        return self.day_name

class Time(models.Model):
    time_name = models.CharField(max_length = 20)

class CartItem(models.Model):
    user_email = models.CharField(max_length = 50)
    selected_day = models.CharField(max_length = 50)
    breakfast_items = models.CharField(max_length = 100)
    lunch_items = models.CharField(max_length = 100)
    dinner_items = models.CharField(max_length = 100)
    order_id = models.CharField(max_length = 20, null = True, blank = True)
    order_date = models.CharField(max_length = 20, null = True, blank = True)
    order_time = models.CharField(max_length = 10, blank = True, null = True)
    # day_price = models.CharField(max_length = 10, blank = True, null = True)