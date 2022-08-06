from users.models import NewUser
from .serializers import SignUpSerializer, UpdateUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# logout
from django.contrib.auth import logout



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"user":"logout"})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def registration(req):
    serializer = SignUpSerializer(data=req.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    data = {}
    data['response'] = 'Successfuly registered a new user.'
    data['email'] = user.email
    data['id'] = user.id
    dataForEmail = {
        'subject':"Verify your email",
        "email":data['email']
    }
    Util.send_email(data=dataForEmail)
    return Response(data, status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(req,id):
    try:
        user = NewUser.objects.get(pk=id)
    except:
        return Response({"massage":"user does not exist"},status.HTTP_400_BAD_REQUEST)
    else:    
        if user.email_is_verify == True:
            return Response({"massage":"error"},status.HTTP_400_BAD_REQUEST)
        user.delete() 
        return Response({"massage":"account deleted"},status.HTTP_200_OK)


@api_view(['POST'])
def validateOTP(req):
    try:
        data=req.data
        email = data['email']
        otp = data['otp']
        user = NewUser.objects.filter(email=email)
        if not user.exists():
            return Response({"massage":"user does not exist"},status.HTTP_400_BAD_REQUEST)
        if user[0].otp != otp:
            return Response({"massage":"wrong otp"},status.HTTP_400_BAD_REQUEST)
        user = user.first()
        user.email_is_verify = True
        user.otp = None
        user.is_active = True
        user.save()
        user2 = NewUser.objects.get(email=email)
        tokens = get_tokens_for_user(user2)
        return Response({"massage":"account verified","refresh":tokens['refresh'],"access":tokens['access']},status.HTTP_200_OK)
    except:
        return Response({"massage":"not a valid body"},status.HTTP_400_BAD_REQUEST)    


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(req):
    try:
        user = req.user
        user2 = NewUser.objects.get(pk=user.id)
        serializer = UpdateUserSerializer(user2 ,data = req.data)
        if serializer.is_valid():
            serializer.update(user2, serializer.validated_data)
            data = {}
            data['massage'] = 'Successfuly updated.'
            return Response(data,status=status.HTTP_200_OK)
        else:
            data = serializer.errors 
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"massage":"except"},status.HTTP_400_BAD_REQUEST)
