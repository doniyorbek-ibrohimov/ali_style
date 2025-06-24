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

            context={
                'cart_items':cart_items,
                'total_sum':total_sum,
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
