from django.contrib import admin
from django.urls import path, include
from . import views
from .views import Api, Rpiinfo

urlpatterns = [
    path('activate/<str:a>', views.activate, name='activate'),
    path('api', Api.as_view()),
    path('checklogin', views.checklogin, name='checklogin'),
    path('clicommanddelete/<int:id>', views.clicommanddelete, name='clicommanddelete'),
    path('clicommandedit/<int:id>', views.clicommandedit, name='clicommandedit'),
    path('clicommandedit', views.clicommandedit, name='clicommandedit'),
    path('clicommandnew', views.clicommandnew, name='clicommandnew'),
    path('clicommands', views.clicommands, name='clicommands'),
    path('home', views.home, name='home'),
    #	path('myaccount/<int:id>', views.myaccount, name='myaccount'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('password', views.password, name='password'),
    path('register', views.register, name='register'),
    path('register_thanks', views.register_thanks, name='register_thanks'),
    path('rpiclicommand', views.rpiclicommand, name='rpiclicommand'),
    path('rpiedit/<int:id>', views.rpiedit, name='rpiedit'),
    path('rpiedit', views.rpiedit, name='rpiedit'),
    path('rpiinfo/<int:id>', Rpiinfo.as_view()),
    path('rpilogline', views.rpilogline, name='rpilogline'),
    path('newnetworkedit', views.newnetworkedit, name='newnetworkedit'),
    path('newnetworks', views.newnetworks, name='newnetworks'),
    path('newrpi', views.newrpi, name='newrpi'),
    path('settings', views.settings, name='settings'),
    path('useredit/<int:id>', views.useredit, name='useredit'),
    path('useredit', views.useredit, name='useredit'),
    path('users', views.users, name='users'),
    path('xnewrpi', views.xnewrpi, name='xnewrpi'),
    path('xrpis', views.xrpis, name='xrpis'),
    path('nextcloud', views.nextcloud, name='nextcloud'),
]
