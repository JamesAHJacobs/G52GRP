from .models import Trade
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

'''
Rahul Soni, Psyrs11

This page defines what different Django 'Views" are supposed to do. These views are called based on the URLs defined in
the urls.py file.



'''

'''

trade_list is the main view, which first checks if the user is successfully logged in. If they are, it loads the trade
objects and returns a Django render comprising of the trades and the trade_list template.

If they are not authenticated, it instead redirects them to the login page.

'''
def trade_list(request, part='1'):
    if request.user.is_authenticated:
        return render(request, 'PTA/trade_list.html', {'part': part})
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'auth.html', c)

'''

Directs a user to the login page

'''
def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'auth.html', c)

'''

This method does one of two things depending on whether it was called with a POST. If it was, it means the user was
on the change password page and submitted the form. In this case, it checks that the form is valid and then changes the
specified user's details and updates their authentication status. It then redirects them to the login page.

If it was not called with POST it means the user is trying to access the change password page. In this case, we return a
Django render comprising of the password change form (locked to the current user) and the change_password template page

'''

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            c = {}
            c.update(csrf(request))
            return render(request, 'auth.html', c)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


'''

This view handles the actual login attempt - if the data is valid the user object will not be None and we can therefore
redirect them to the logged in page which will then redirect them on.

If the user object is null however, the login provided was invalid and the the user will be told so.

'''
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')


'''

This is the view called by the successful login attempt from auth_view. It double checks that the user is authenticated
and then returns a Django render comprising of the logged in page and the users name, letting them know they are in.

'''

def loggedin(request):
    if request.user.is_authenticated:
        return render(request, 'loggedin.html', {'full_name': request.user.username})
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'auth.html', c)

'''

This is the view called by the bad login attempt from auth_view. It returns a render of the invalid login page.

'''
def invalid_login(request):
    return render(request, 'invalid.html')


'''

This view logs a user out. The Django logout method removes their authentication and current session data, and they are
redirected to a landing page.

'''
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


'''

This view used to render the blotter page, but both pages have since been moved into one, and so it now effectively
takes a user to the trade_history page and then calls the appropriate client side code to show the blotter instead of
the pending trades. However it is left here for auditing purposes. As most other views, if the user is not logged in
they are redirected.

'''
def trade_history(request):
    if request.user.is_authenticated:
        trades = Trade.objects.filter(Date__lte=timezone.now()).order_by('Date')
        return render(request, 'PTA/trade_history.html', {'trades': trades})
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'auth.html', c)


'''

This page renders the user settings page from where a password can be changed if the user is logged in, otherwise it
redirects to the login page.

'''
def user_settings(request):
    if request.user.is_authenticated:
        return render(request, 'PTA/user_settings.html')
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'auth.html', c)

