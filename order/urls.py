from django.urls import path
from .views import *


urlpatterns=[
    path('my-cart',CartView.as_view(),name="cart"),
    path('add-to-cart/<int:pk>/',AddToCartView.as_view(),name='add-to-cart'),
    path('remove-from-cart/<int:pk>/',RemoveFromCart.as_view(),name='remove_from_cart'),
    path('cart-amount-add/<int:pk>/',CartAmountAdd.as_view(),name='cart-amount-add'),
    path('cart-amount-subtract/<int:pk>/',CartAmountSubtract.as_view(),name='cart-amount-subtract'),
    path('payment/',OrderView.as_view(),name='payment'),
    path('favorite_item/<int:pk>/',FavoriteView.as_view(),name="favorite"),
    path('wishlist/',WishListView.as_view(),name="wishlist"),
    path('favorite/delete/<int:product_id>/',delete_favorite, name='delete_favorite'),
]