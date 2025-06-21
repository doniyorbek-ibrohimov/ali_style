from django.urls import path
from .views import *

urlpatterns=[
    path('register/',RegisterView.as_view(),name="register"),
    path('register-confirm/',RegisterConfirmView.as_view(),name='register-confirm'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView,name='logout'),
]