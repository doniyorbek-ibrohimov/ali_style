from tkinter.font import names

from django.urls import path
from .views import *

urlpatterns=[
    path('register/',RegisterView.as_view(),name="register"),
    path('register-confirm/',RegisterConfirmView.as_view(),name='register-confirm'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView,name='logout'),
    path('my-orders',OrdersView.as_view(),name='orders'),
    path('prodile/',ProfileView.as_view(),name='profile'),
    path('address/',AddressView.as_view(),name="address"),
    path('settings/',SettingsView.as_view(),name="settings"),
]