# # TODO: Imports

# from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.contrib import messages
from django.template import loader

from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model

from .validate import unauth_user_permission
from .email_domain import validate_domain
from .cart_obj_detail import cprod_details
from .dwod_genid import gen_od_id

from .models import Product, Day, Category, CartItem

from datetime import datetime, date

# # TODO: CREATE YOUR VIEWS HERE #

User = get_user_model()

# TODO: Load the templates 
front_page = loader.get_template('frontpage.html')
login_page = loader.get_template('login.html')
signup_page = loader.get_template('register.html')

home_page = loader.get_template('main.html')
profile_page = loader.get_template('profile.html')
create_menu_page = loader.get_template('menu.html')
item_selection_page = loader.get_template('selectitem.html')

item_cart_page = loader.get_template('cart.html')
order_list_page = loader.get_template('your_orders.html')

# TODO: creating view functions

# Front page
@unauth_user_permission
def index(request):
    return HttpResponse(front_page.render({}, request))

# user registration
@unauth_user_permission
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password_again = request.POST['password_again']

        # checking if both passwords are same
        if password == password_again:
            # checking if entered email is already registered
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email already registered')
                return HttpResponseRedirect(reverse('register'))
            # checking if entered email is already registered
            elif User.objects.filter(phone_number = phone_number).exists():
                messages.info(request, 'Phone already registered')
                return HttpResponseRedirect(reverse('register'))
            
            else:
                # if new email and phone number save as user in User table
                user = User.objects.create_user(email = email, name = name, phone_number = phone_number, password = password)
                user.save()
                request.session['user_name'] = user.name
                return HttpResponseRedirect('/login/')
            
        else:
            messages.info(request, "Password does not match")
            return HttpResponseRedirect(reverse('register'))
        
    else:      
        return HttpResponse(signup_page.render({}, request))

# user login
@unauth_user_permission
def login(request):
    if request.method == 'POST':
        # getting email and password from the logiin form to valuidte authentication
        email = request.POST['email']
        password = request.POST['password']
        # authenticate from User table using given parameters
        user = auth.authenticate(email = email, password = password)

        # checking existence of user
        if user is not None:
            auth.login(request, user)

            # adding logged in user email to the session
            request.session['user_email'] = user.email

            print("Logged in User email : ", request.session.get('user_email'))
            
            return HttpResponseRedirect('/homepage/')

        else:
            messages.info(request, "invalid credentials !")
            return HttpResponseRedirect(reverse('login'))
        
    else:
        return HttpResponse(login_page.render({}, request))
    

# user logout
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# Home page
def homepage(request):

    # checking user role through function
    email = request.session.get('user_email')

    if email is not None:        
        role = validate_domain(email)
        print(f"Logged in user is a : ", role)

        # loading the Product table to display the items
        items = Product.objects.all()

        context = {
            'role':role,
            'items':items,
        }
        return HttpResponse(home_page.render(context, request))
    
    else:
        return HttpResponse(home_page.render({}, request))
    
def profile(request):
    email = request.session.get('user_email')
    if email is not None:
        user = User.objects.get(email = email)
    
        context = {
            'user':user,
        }

        return HttpResponse(profile_page.render(context, request))
    else:
        return HttpResponse(profile_page.render({}, request))
    
def create_menu(request):
    days = Day.objects.all().values()
    context = {
        'days':days
    }
    return HttpResponse(create_menu_page.render(context, request))

def item_selection(request, day_name):

    if request.user.is_authenticated:

        selected_day = day_name
        print(selected_day)

        breakfast_items = Product.objects.filter(item_cat = Category.objects.get(id = 1))
        print(breakfast_items)

        lunch_items = Product.objects.filter(item_cat = Category.objects.get(id = 2))
        print(breakfast_items)

        dinner_items = Product.objects.filter(item_cat = Category.objects.get(id = 3))
        print(breakfast_items)

        context = {
            'selected_day':selected_day,
            'breakfast_items':breakfast_items,
            'lunch_items':lunch_items,
            'dinner_items':dinner_items
        }

        return HttpResponse(item_selection_page.render(context, request))
    
    else:
        return HttpResponseRedirect(reverse('homepage'))
    

def save_items_by_day(request):

    if request.method == 'POST':
        selected_day = request.POST.get('selected_day', False)
        breakfast_list = request.POST.get('breakfast_list', False)
        lunch_list = request.POST.get('lunch_list', False)
        dinner_list = request.POST.get('dinner_list', False)
        print(selected_day, breakfast_list, lunch_list, dinner_list)

        email = request.session.get('user_email')

        cart_item_by_day = CartItem(user_email = email, selected_day = selected_day, breakfast_items = breakfast_list, lunch_items = lunch_list, dinner_items = dinner_list)
        cart_item_by_day.save()

        return HttpResponseRedirect('/cart/')

    else:
        messages.info(request, "Some unknown error has occurred")
        return HttpResponseRedirect(reverse('create_menu'))

def cart(request):
    
    email = request.session.get('user_email')

    ## MONDAY ##
    try:
        mon_cart_lst = CartItem.objects.get(user_email = email, selected_day = 'Monday', order_id = None)
        if mon_cart_lst.order_id is None:
            mb = mon_cart_lst.breakfast_items
            monday_breakfast, mbtprice = cprod_details(mb)
            print(monday_breakfast, mbtprice)

            ml = mon_cart_lst.lunch_items
            monday_lunch, mltprice = cprod_details(ml)
            print(monday_lunch, mltprice)

            md = mon_cart_lst.dinner_items
            monday_dinner, mdtprice = cprod_details(md)
            print(monday_dinner, mdtprice)

            monday_total_price = mbtprice+mltprice+mdtprice
            print(monday_total_price)
    except CartItem.DoesNotExist:
        mon_cart_lst = None
        monday_breakfast = None
        monday_lunch = None
        monday_dinner = None
        mbtprice = None
        mltprice = None
        mdtprice = None
        monday_total_price = 0


    ## TUESDAY ##
    try:
        tues_cart_lst = CartItem.objects.get(user_email = email, selected_day = 'Tuesday', order_id = None)
        if tues_cart_lst.order_id is None:
            tb = tues_cart_lst.breakfast_items
            tuesday_breakfast, tbtprice = cprod_details(tb)
            print(tuesday_breakfast, tbtprice)

            tl = tues_cart_lst.lunch_items
            tuesday_lunch, tltprice = cprod_details(tl)
            print(tuesday_lunch, tltprice)

            td = tues_cart_lst.dinner_items
            tuesday_dinner, tdtprice = cprod_details(td)
            print(tuesday_dinner, tdtprice)

            tuesday_total_price = tbtprice+tltprice+tdtprice
            print(tuesday_total_price)
    except CartItem.DoesNotExist:
        tues_cart_lst = None
        tuesday_breakfast = None
        tuesday_lunch = None
        tuesday_dinner = None
        tbtprice = None
        tltprice = None
        tdtprice = None
        tuesday_total_price = 0

    ## WEDNESDAY ##
    try:
        wed_cart_lst = CartItem.objects.get(user_email = email, selected_day = 'Wednesday', order_id = None)
        if wed_cart_lst.order_id is None:
            wb = wed_cart_lst.breakfast_items
            wednesday_breakfast, wbtprice = cprod_details(wb)
            print(wednesday_breakfast, wbtprice)

            wl = wed_cart_lst.lunch_items
            wednesday_lunch, wltprice = cprod_details(wl)
            print(wednesday_lunch, wltprice)

            wd = wed_cart_lst.dinner_items
            wednesday_dinner, wdtprice = cprod_details(wd)
            print(wednesday_dinner, wdtprice)

            wednesday_total_price = wbtprice+wltprice+wdtprice
            print(wednesday_total_price)
    except CartItem.DoesNotExist:
        wed_cart_lst = None
        wednesday_breakfast = None
        wednesday_lunch = None
        wednesday_dinner = None
        wbtprice = None
        wltprice = None
        wdtprice = None
        wednesday_total_price = 0


    ## THURSDAY ##
    try:
        thurs_cart_lst = CartItem.objects.get(user_email = email, selected_day = 'Thursday', order_id = None)
        if thurs_cart_lst.order_id is None:
            thb = thurs_cart_lst.breakfast_items
            thursday_breakfast, thbtprice = cprod_details(thb)
            print(thursday_breakfast, thbtprice)

            thl = thurs_cart_lst.lunch_items
            thursday_lunch, thltprice = cprod_details(thl)
            print(thursday_lunch, thltprice)

            thd = thurs_cart_lst.dinner_items
            thursday_dinner, thdtprice = cprod_details(thd)
            print(thursday_dinner, thdtprice)

            thursday_total_price = thbtprice+thltprice+thdtprice
            print(thursday_total_price)
    except CartItem.DoesNotExist:
        thurs_cart_lst = None
        thursday_breakfast = None
        thursday_lunch = None
        thursday_dinner = None
        thbtprice = None
        thltprice = None
        thdtprice = None
        thursday_total_price = 0


    ## FRIDAY ##
    try:
        fri_cart_lst = CartItem.objects.get(user_email = email, selected_day = 'Friday', order_id = None)
        if fri_cart_lst.order_id is None:
            fb = fri_cart_lst.breakfast_items
            friday_breakfast, fbtprice = cprod_details(fb)
            print(friday_breakfast, fbtprice)

            fl = fri_cart_lst.lunch_items
            friday_lunch, fltprice = cprod_details(fl)
            print(friday_lunch, fltprice)

            fd = fri_cart_lst.dinner_items
            friday_dinner, fdtprice = cprod_details(fd)
            print(friday_dinner, fdtprice)

            friday_total_price = fbtprice+fltprice+fdtprice
            print(friday_total_price)
    except CartItem.DoesNotExist:
        fri_cart_lst = None
        friday_breakfast = None
        friday_lunch = None
        friday_dinner = None
        fbtprice = None
        fltprice = None
        fdtprice = None
        friday_total_price = 0


    ## SATURDAY ##
    try:
        sat_cart_lst = CartItem.objects.get(user_email = email, selected_day = 'Saturday', order_id = None)
        if sat_cart_lst.order_id is None:
            sab = sat_cart_lst.breakfast_items
            saturday_breakfast, sabtprice = cprod_details(sab)
            print(saturday_breakfast, sabtprice)

            sal = sat_cart_lst.lunch_items
            saturday_lunch, saltprice = cprod_details(sal)
            print(saturday_lunch, saltprice)

            sad = sat_cart_lst.dinner_items
            saturday_dinner, sadtprice = cprod_details(sad)
            print(saturday_dinner, sadtprice)

            saturday_total_price = sabtprice+saltprice+sadtprice
            print(saturday_total_price)
    except CartItem.DoesNotExist:
        sat_cart_lst = None
        saturday_breakfast = None
        saturday_lunch = None
        saturday_dinner = None
        sabtprice = None
        saltprice = None
        sadtprice = None
        saturday_total_price = 0


    ## SUNDAY ##
    try:
        sun_cart_lst = CartItem.objects.get(user_email = email, selected_day = 'Sunday', order_id = None)
        if sun_cart_lst.order_id is None:
            sub = sun_cart_lst.breakfast_items
            sunday_breakfast, subtprice = cprod_details(sub)
            print(sunday_breakfast, subtprice)
    
            sul = sun_cart_lst.lunch_items
            sunday_lunch, sultprice = cprod_details(sul)
            print(sunday_lunch, sultprice)
    
            sud = sun_cart_lst.dinner_items
            sunday_dinner, sudtprice = cprod_details(sud)
            print(sunday_dinner, sudtprice)
    
            sunday_total_price = subtprice+sultprice+sudtprice
            print(sunday_total_price)
    except CartItem.DoesNotExist:
        sun_cart_lst = None
        sunday_breakfast = None
        sunday_lunch = None
        sunday_dinner = None
        subtprice = None
        sultprice = None
        sudtprice = None
        sunday_total_price = 0


    try:
        total_week_price = monday_total_price + tuesday_total_price + wednesday_total_price + thursday_total_price + friday_total_price + saturday_total_price + sunday_total_price
    except:
        total_week_price = 0
    print(total_week_price)

    request.session['total_price'] = total_week_price
    
    context = {
        # monday
        'monday_breakfast':monday_breakfast,
        'monday_lunch':monday_lunch,
        'monday_dinner':monday_dinner,
        'mbtprice':mbtprice,
        'mltprice':mltprice,
        'mdtprice':mdtprice,
        'monday_total_price':monday_total_price,
        # tuesday
        'tuesday_breakfast':tuesday_breakfast,
        'tuesday_lunch':tuesday_lunch,
        'tuesday_dinner':tuesday_dinner,
        'tbtprice':tbtprice,
        'tltprice':tltprice,
        'tdtprice':tdtprice,
        'tuesday_total_price':tuesday_total_price,
        # wednesday
        'wednesday_breakfast':wednesday_breakfast,
        'wednesday_lunch':wednesday_lunch,
        'wednesday_dinner':wednesday_dinner,
        'wbtprice':wbtprice,
        'wltprice':wltprice,
        'wdtprice':wdtprice,
        'wednesday_total_price':wednesday_total_price,
        # thursday
        'thursday_breakfast':thursday_breakfast,
        'thursday_lunch':thursday_lunch,
        'thursday_dinner':thursday_dinner,
        'thbtprice':thbtprice,
        'thltprice':thltprice,
        'thdtprice':thdtprice,
        'thursday_total_price':thursday_total_price,
        # friday
        'friday_breakfast':friday_breakfast,
        'friday_lunch':friday_lunch,
        'friday_dinner':friday_dinner,
        'fbtprice':fbtprice,
        'fltprice':fltprice,
        'fdtprice':fdtprice,
        'friday_total_price':friday_total_price,
        # saturday
        'saturday_breakfast':saturday_breakfast,
        'saturday_lunch':saturday_lunch,
        'saturday_dinner':saturday_dinner,
        'satprice':sabtprice,
        'satprice':saltprice,
        'satprice':sadtprice,
        'saturday_total_price':saturday_total_price,
        # sunday
        'sunday_breakfast':sunday_breakfast,
        'sunday_lunch':sunday_lunch,
        'sunday_dinner':sunday_dinner,
        'subtprice':subtprice,
        'sultprice':sultprice,
        'sudtprice':sudtprice,
        'sunday_total_price':sunday_total_price,
        # total price for the week
        'total_week_price':total_week_price,
    }
    return HttpResponse(item_cart_page.render(context, request))

def command_order(request):
    email = request.session.get('user_email')
    cart_item = CartItem.objects.filter(user_email = email, order_id = None)
    user = User.objects.get(email = email)
    user_name = user.name
    print(user_name)
    o_id = gen_od_id()
    request.session['order_id'] = o_id
    for item in cart_item:
        o_date = date.today()
        now = datetime.now()
        o_time = now.strftime("%H:%M:%S")
        item.order_id = o_id
        item.order_date = o_date
        item.order_time = o_time
        item.save()
    return HttpResponseRedirect('/your_orders/')

def your_orders(request):
    order_id = request.session.get('order_id')
    total_price = request.session.get('total_price')

    context = {
        'order_id':order_id,
        'total_price':total_price,
    }
    return HttpResponse(order_list_page.render(context, request))
    # return HttpResponse(f"Thank for ordering from DabbaWala !\nYour order with ::\n\tOrder Id: {order_id}\n\tTotal Price: ₹ {total_price}\nhas been confirmed successfully")



last_oid = CartItem.objects.filter(order_id__istartswith = 'DW').last()
print(type(last_oid))
txt = 'DW0001'
print(type(txt[2:]))