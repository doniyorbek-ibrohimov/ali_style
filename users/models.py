from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices


class GENDER(TextChoices):
    MALE='Male','Male'
    FEMALE='Female','Female'


class User(AbstractUser):
    phone=models.CharField(max_length=13,unique=True)
    gender=models.CharField(max_length=10,choices=GENDER.choices)
    birth_date=models.DateField(blank=True,null=True)
    confirmation_code=models.CharField(max_length=10)
    confirmed=models.BooleanField(default=False)
    country=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)




