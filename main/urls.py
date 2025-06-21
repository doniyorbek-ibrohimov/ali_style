from django.urls import path

from .views import *

urlpatterns=[
    path('',HomeView.as_view(),name='home'),
    path('categories/<int:pk>/',CategoryView.as_view(),name="category"),
    path('products/',ProductsView.as_view(),name="products"),
    path('product/<int:pk>/',ProductView.as_view(),name="product")
]