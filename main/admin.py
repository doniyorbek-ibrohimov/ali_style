from django.contrib import admin
from .models import *

admin.site.register(
    [
        Category,SubCategory,Image,Discount,Banner,Product,Review
    ]
)
