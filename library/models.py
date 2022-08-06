from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
class Type(models.Model):
    loanDays = models.IntegerField(verbose_name='days to loan the book')
    loanFee = models.IntegerField(verbose_name='fee per day')
    status = models.BooleanField(default=True)
    _id = models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return f"{self._id}   ___________ {self.status}"


class Book(models.Model):
    name = models.CharField(max_length=60,null=True)
    type = models.ForeignKey(Type,on_delete=models.SET_NULL,null=True)
    author = models.CharField(max_length=20,null=True)
    yearPublished = models.CharField(max_length=4,null=True)
    category = models.CharField(max_length=10,null=True)
    imgURL = models.TextField(max_length=250,null=True,blank=True) # Default !
    info = models.TextField(max_length=2000,null=True,blank=True)
    cost = models.IntegerField()
    copies = models.IntegerField()
    status = models.BooleanField(default=True)
    _id = models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return f"{self._id} {self.name}"


class Loan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    start_date = models.CharField(max_length=13,null=True)
    return_date = models.CharField(max_length=13,null=True)
    status = models.IntegerField(default=2341)
    _id = models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return f"{self._id} {self.status}"
