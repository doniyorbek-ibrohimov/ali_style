from django.shortcuts import render,redirect

from django.views import View

class HomeView(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.confirmed==git initgTrue:
            return render(request,'index.html')
        return render(request,'index-2.html')
