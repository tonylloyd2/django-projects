from unicodedata import name
from django.urls import path
from . import views as UserViews

urlpatterns = [
    path('login/',UserViews.login,name='login'),
    path('logout/',UserViews.logout,name='logout'),
    path('register/',UserViews.register,name="register"),
    path('account-settings/',UserViews.AccountSettings,name='AccountSettings')
]
