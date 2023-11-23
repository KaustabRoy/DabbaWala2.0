from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .views import *

def unauth_user_permission(view_func):
    def check(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return view_func(request, *args, **kwargs)
    return check

