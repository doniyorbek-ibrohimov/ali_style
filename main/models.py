from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import *

class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/categories',blank=True,null=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/categories',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=10,blank=True,null=True)
    price=models.FloatField(validators=[MinValueValidator(0.0)])
    description=models.TextField()
    delivery_time=models.CharField(max_length=100)
    guarantee=models.CharField(blank=True,null=True,max_length=100)
    rating=models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(5.0)],blank=True,null=True)
    sub_category=models.ForeignKey(SubCategory,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Image(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/products')

    def __str__(self):
        return self.product.name


class Discount(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    percentage=models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(100.0)])
    start_date=models.DateField()
    end_date=models.DateField(blank=True,null=True)
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name




class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    comment=models.TextField(blank=True,null=True)
    rate=models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.name}"

class Banner(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/banners')
    sub_category=models.ForeignKey(SubCategory,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


