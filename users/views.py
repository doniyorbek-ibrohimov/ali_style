from django.shortcuts import render,redirect
from django.views import View
from .models import *
from order.models import *
from random import randint
from django.contrib.auth import login,logout,authenticate

class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        if request.POST.get('password1')!=request.POST.get('password2') or request.POST.get('phone') in User.objects.values_list('phone',flat=True):
            return redirect('register')
        confirmation_code=randint(10000,99999)
        print(confirmation_code)
        user=User.objects.create_user(
            username=request.POST.get('phone'),
            password=request.POST.get('password1'),
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            gender=request.POST.get('gender'),
            country=request.POST.get('country'),
            city=request.POST.get('city'),
            phone=request.POST.get('phone'),
            confirmation_code=confirmation_code,
        )
        login(request, user)
        return redirect('register-confirm')

class RegisterConfirmView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,'register-confirmation.html')
        return redirect('register')
    def post(self,request):
        if request.user.is_authenticated:
            user=request.user
            if request.POST.get('code')==user.confirmation_code:
                user.confirmed=True
                user.save()
                return redirect('home')
            return redirect('register-confirm')
        return redirect('register')

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        user=authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        return redirect('login')


def LogoutView(request):
    logout(request)
    return redirect('login')

class OrdersView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed:
            orders=Order.objects.filter(user=request.user)
            context={
                'orders':orders
            }
            return render(request,'profile-orders.html',context)

class ProfileView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed:
            return render(request,'profile-main.html')
        return redirect('login')

class AddressView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed:
            return render(request,'profile-address.html')
        return redirect('login')


class SettingsView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed:
            return render(request,'profile-settings.html')
        return redirect('login')

    def post(self,request):
        if request.user.is_authenticated and request.user.confirmed:
            user=request.user
            user.first_name=request.POST.get('first_name')
            user.last_name=request.POST.get('last_name')
            user.phone=request.POST.get('phone')
            user.country=request.POST.get('country')
            user.city=request.POST.get('city')
            user.save()
            return redirect('settings')
        return redirect('login')

