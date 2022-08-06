from datetime import datetime , timedelta
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.core import serializers
from library.models import Book, Loan
from django.db.models import Q
from users.models import NewUser

# user can get the relevant books
@api_view(['GET'])
def get_relevant(request ,format=None):
    books_relevant = []
    books = Book.objects.order_by("name").select_related("type").values_list('_id','name','author','yearPublished','category','imgURL','info','type__loanDays','type__loanFee').filter(status=True, type__status=True).filter(Q(copies__gte=1)) 
    for book in books:
        newDict = {
            "id":book[0],
            "name":book[1],
            "author":book[2],
            "yearPublished":book[3],
            "category":book[4],
            "imgURL":book[5],
            "info":book[6],
            "fee_per_day":book[7],
            "day_to_loan":book[8]
        }
        books_relevant.append(newDict)
    return JsonResponse({"books":books_relevant})

# user can get all his loans
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_loans_or_add_new(request):
    if request.method == 'GET':
        user = request.user
        loans = Loan.objects.order_by("status").select_related("book").select_related("type").values_list('start_date', 'return_date','book__name','book__author','book__yearPublished','book__category','status', 'book__type__loanDays', 'book__type__loanFee','book__imgURL','book__info','book_id').filter(user_id=user.id)
        if  (not loans.exists()):
            return JsonResponse({"massage":"no such loans!"})
        active_loans = []
        history_loans = []
        for loan in loans:
            print(loan)
            if loan[6] == 2341:
                active_loans.append({ "id":loan[11],
                "book_name":loan[2], "author":loan[3], "year_published":loan[4],
                "category":loan[5], "max_days_to_loan":loan[7], "max_fee_per_day":loan[8],
                "date_of_start":loan[0], "date_of_return":loan[1], "status":loan[6], "img":loan[9],"info":loan[10]
                })
            else:history_loans.append({ "id":loan[11],
                "book_name":loan[2], "author":loan[3], "year_published":loan[4],
                "category":loan[5], "max_days_to_loan":loan[7], "max_fee_per_day":loan[8],
                "date_of_start":loan[0], "date_of_return":loan[1], "status":loan[6], "img":loan[9],"info":loan[10]
                })    
        return JsonResponse({"active_loans":active_loans, "history_loans":history_loans})

    if request.method == 'POST':
        user = request.user
        userOO = NewUser.objects.get(pk=user.id)
        try:
            data = json.loads(request.body)
            b = Book.objects.get(_id=data['book_id'])
        except:return JsonResponse({"massage":"not a valid body"})
        else:
            checking = serializers.serialize("json",Loan.objects.filter(user__id=user.id, status=2341))
            if (len(json.loads(checking)) >= 3):
                return JsonResponse({"massage":"user has more than 3 books at the time..."})
            checking = serializers.serialize("json",Loan.objects.filter(user__id=user.id, status=2341, book___id=data['book_id']))
            if (len(json.loads(checking)) >= 1):
                return JsonResponse({"massage":"user already took this book..."})
            b.copies -= 1
            b.save()
            days_to_loan = b.type.loanDays
            now = datetime.now()
            delta = timedelta(days=days_to_loan)
            date_of_return= now + delta
            if date_of_return.strftime('%a')=="Sat":
                delta = timedelta(days=days_to_loan+1)
                date_of_return= now + delta
                strReturn = date_of_return.strftime('%d-%m-%Y, %H:%M:%S')
                strStrat = now.strftime('%d-%m-%Y, %H:%M:%S')
                l = Loan.objects.create(user=userOO, book=b ,start_date=strStrat, return_date=strReturn)
                loan_serialized = serializers.serialize("json", Loan.objects.filter(pk=l._id))
                return HttpResponse(loan_serialized, content_type='application/json')
            else:
                strReturn = date_of_return.strftime('%d-%m-%Y, %H:%M:%S')
                strStrat = now.strftime('%d-%m-%Y, %H:%M:%S')
                l = Loan.objects.create(user=userOO, book=b ,start_date=strStrat, return_date=strReturn)
                loan_serialized = serializers.serialize("json", Loan.objects.filter(pk=l._id))
                return HttpResponse(loan_serialized, content_type='application/json')

# user can return a book
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def return_book(request, id):
    user = request.user
    try:
        loan = Loan.objects.get(user__id=user.id, book___id=id, status=2341)
    except:
        return Response({"message":"no active loan with this book..."},status.HTTP_400_BAD_REQUEST)
    else:
        no_str = datetime.strptime(loan.return_date,'%d-%m-%Y, %H:%M:%S')
        today = datetime.now()
        delta = today - no_str
        loan.status = delta.days
        loan.save()
        book = Book.objects.get(pk=id)
        book.copies += 1
        book.save()
        loan_updated = serializers.serialize("json", Loan.objects.filter(pk=loan._id))
        return HttpResponse(loan_updated, content_type='application/json')
