from django.urls import path
from . import views

urlpatterns = [
 path('books/',views.get_relevant),
 path('loans/',views.get_loans_or_add_new),
 path('loans/<id>/',views.return_book),
]