from django.core.paginator import Paginator
from django.db.models import Avg,Sum
from django.shortcuts import render,redirect,get_object_or_404
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

class CategoryView(View):
    def get(self,request,pk):
        if request.user.is_authenticated and request.user.confirmed:
            category=get_object_or_404(Category,pk=pk)
            context={
                'category':category
            }
            return render(request,'category.html',context)
        return redirect('login')


class ProductsView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
            products = Product.objects.all()
            countries = products.values_list('country', flat=True).distinct()

            sub_category_id = request.GET.get('sub_category')
            country = request.GET.get('country')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')

            print("sub_category_id:", sub_category_id)
            print("country:", country)
            print("min_price:", min_price)
            print("max_price:", max_price)

            sub_category = None

            if sub_category_id:
                sub_category = get_object_or_404(SubCategory, pk=sub_category_id)
                products = products.filter(sub_category=sub_category)

            if country:
                products = products.filter(country=country)

            if min_price:
                products = products.filter(price__gte=min_price)

            if max_price:
                products = products.filter(price__lte=max_price)

            page_number=request.GET.get('page')
            paginator=Paginator(products,4)
            page_obj=paginator.get_page(page_number)

            context = {
                'products': page_obj,
                'sub_category': sub_category,
                'countries': countries,
                'min_price': min_price,
                'max_price': max_price,
                'choice_country': country,
                'page_obj':page_obj
            }
            return render(request, 'products_grid.html', context)
        return redirect('login')

class ProductView(View):
    def get(self,request,pk):
        if request.user.is_authenticated and request.user.confirmed==True:
            product=get_object_or_404(Product,pk=pk)

            r_as_per=(product.rating if product.rating else 5) * 20

            context={
                'product':product,
                'r_as_per':r_as_per,
            }
            return render(request,'product-details.html',context)
        return redirect('login')
    def post(self,request,pk):
        if request.user.is_authenticated and request.user.confirmed == True:
            product=get_object_or_404(Product,pk=pk)
            review=Review.objects.create(
                user=request.user,
                product=product,
                rate=request.POST.get('rating') if request.POST.get('rating') else 5,
                comment=request.POST.get('comment'),
            )
            rating_sum=product.review_set.all().aggregate(Sum('rate',))['rate__sum']
            rating_count=product.review_set.all().count()
            product.rating=rating_sum / rating_count if rating_count > 0 else 1
            product.save()


            return self.get(request,pk)




