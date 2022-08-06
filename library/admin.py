from django.contrib import admin
from .models import Type, Book, Loan

admin.site.register(Book)
admin.site.register(Type)
admin.site.register(Loan)
