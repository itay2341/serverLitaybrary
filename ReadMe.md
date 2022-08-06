

(pip install virtualenv)

py -m virtualenv myenv

.\myenv\Scripts\Activate

pip install django

django-admin startproject backend .

django-admin startapp users

INSTALLED_APPS = users

pip install djangorestframework
pip install djangorestframework-simplejwt 

INSTALLED_APPS = rest_framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
If you wish to use localizations/translations, simply add rest_framework_simplejwt to INSTALLED_APPS.

now... customization the users.

pip install django-cors-headers

