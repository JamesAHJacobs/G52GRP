from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

'''
Rahul Soni, Psyrs11

This file defines which view is called when a client tries to access a page. For details on what the views do, check
views.py

'''
urlpatterns = [
    url(r'^$', views.trade_list, name='trade_list'),
    #url(r'^channel/$', views.channel),
    #url(r'', views.home),
    url(r'^trade_list/$', views.trade_list, name ='trade_list'),
    url(r'^trade_list/([12])/$', views.trade_list, name ='trade_list'),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/auth/$', views.auth_view),
    url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    url(r'^accounts/loggedin/$', views.loggedin),
    url(r'^accounts/invalid/$', views.invalid_login),
    url(r'^trade_history/$', views.trade_history, name='trade_history'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^user_settings', views.user_settings, name='user_settings'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

