from django.shortcuts import render,redirect,get_object_or_404
from django.template.context_processors import request
from django.views import View
from django.db.models import Sum,ExpressionWrapper,F,FloatField
from .models import *

class CartView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed==True:
            cart_items=CartItem.objects.filter(user=request.user).annotate(
                total_price=ExpressionWrapper(
                    F('product__price') * F('amount'),output_field=FloatField()
                )
            )
            total_sum=cart_items.aggregate(Sum('total_price'))['total_price__sum']
            favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

            context={
                'cart_items':cart_items,
                'total_sum':total_sum,
                'favorites':favorites
            }
            return render(request,'cart.html',context)
        return redirect('login')


class AddToCartView(View):
    def get(self,request,pk):
        if request.user.is_authenticated and request.user.confirmed==True:
            cart_items=CartItem.objects.filter(user=request.user,product=get_object_or_404(Product,pk=pk))
            if cart_items.exists():
                cart_item=cart_items.first()
                cart_item.amount +=1
                cart_item.save()
                return redirect('cart')
            CartItem.objects.create(
                user=request.user,
                product=get_object_or_404(Product,pk=pk)
            )
            return redirect('product',pk=pk)
        return redirect('login')

class RemoveFromCart(View):
    def get(self,request,pk):
        if request.user.is_authenticated and request.user.confirmed == True:
            cart_item=get_object_or_404(CartItem,pk=pk)
            cart_item.delete()
            return redirect('cart')
        return redirect('login')

class CartAmountAdd(View):
    def get(self,request,pk):
        if request.user.is_authenticated and request.user.confirmed == True:
            cart_item=get_object_or_404(CartItem,pk=pk)
            cart_item.amount+=1
            cart_item.save()
            return redirect('cart')
        return redirect('login')

class CartAmountSubtract(View):
    def get(self,request,pk):
        if request.user.is_authenticated and request.user.confirmed == True:
            cart_item=get_object_or_404(CartItem,pk=pk)
            if cart_item.amount==1:
                return redirect('remove_from_cart',pk=pk)
            cart_item.amount -=1
            cart_item.save()
            return redirect('cart')
        return redirect('login')

class OrderView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed:
            return render(request,'payment.html')
        return redirect('login')

    def post(self,request):
        if request.user.is_authenticated and request.user.confirmed:
            cart_items=CartItem.objects.filter(user=request.user)
            order=Order.objects.create(
                user=request.user,
                delivery_type=request.POST.get('delivery'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                phone=request.POST.get('phone'),
                country=request.POST.get('country'),
                city=request.POST.get('city'),
                address=request.POST.get('address'),
            )
            total_price=0
            for cart_item in cart_items:
                total_price=cart_item.product.price * cart_item.product.amount
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    amount=cart_item.amount,
                )
            cart_items.delete()
            if request.POST.get('delivery')=='Fast':
                total_price += 20

            order.total_price=total_price
            order.save()
            return redirect('cart')
        return redirect('login')


class FavoriteView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not request.user.confirmed:
            return redirect('login')

        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
        product = cart_item.product

        favorite = Favorite.objects.filter(user=request.user, product=product).first()
        if favorite:
            favorite.delete()
        else:
            Favorite.objects.create(user=request.user, product=product)

        return redirect('cart')



class WishListView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed:
            favorite_products=Product.objects.filter(favorite__user=request.user)
            context={
                'favorite_products':favorite_products
            }
            return render(request,'wishlist.html',context)
        return redirect('login')


def delete_favorite(request,product_id):
    favorite=Favorite.objects.filter(user=request.user,product_id=product_id)
    favorite.delete()
    return redirect('wishlist')