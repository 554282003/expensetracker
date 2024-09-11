from . views import RegistrationView,loginView,UsernameValidation,LogOutView,EmailValidation,VerficationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', loginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('user-validation/', csrf_exempt(UsernameValidation.as_view()), name='Usernamevalidation'),
    path('email-validation/', csrf_exempt(EmailValidation.as_view()), name='Emailvalidation'),
    path('activate/<uidb64>/<token>', VerficationView.as_view(), name='activate'),
]
