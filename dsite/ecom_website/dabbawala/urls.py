from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('homepage/', views.homepage, name = 'homepage'),
    path('profile/', views.profile, name = 'profile'),
    path('create_menu/', views.create_menu, name = 'create_menu'),
    path('create_menu/item_selection/<str:day_name>/', views.item_selection, name = 'select_items_fortheday'),
    path('save_items_by_day/', views.save_items_by_day, name = 'save_items_by_day'),
    path('cart/', views.cart, name = 'cart'),
    path('cart/command_order/', views.command_order, name = 'order_create'),
    path('your_orders/', views.your_orders, name = 'your_orders'),
]