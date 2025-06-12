from django.shortcuts import render,redirect
from django.views import View
from .models import *


class HomeView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed==True:
            categories=Category.objects.all()
            banners=Banner.objects.all()
            discounts=Discount.objects.filter(active=True)
            products=Product.objects.all()[:12]
            context={
                'categories':categories,
                'banners':banners,
                'discounts':discounts,
                'products':products
            }
            return render(request,'index.html',context)
        return render(request,'index-2.html')
