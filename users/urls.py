from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'users'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.registration,name='register'),
    path('email_verify/',views.validateOTP,name='email_verify'),
    path('delete/<id>/', views.delete_user,name="delete_user"),
    path('user/update/',views.update_user ,name="update_user"),
    path('logout/',views.logout_view ,name="logout"),
]