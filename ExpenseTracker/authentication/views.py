# from django.contrib.auth.models import User
# >>> User.objects.all().delete()
# from validate_email import validate_email

from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from email_validator import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.utils.encoding import force_str
from django.urls import reverse
from .utilis import token_generate
from django.contrib import auth

# Create your views here.

class UsernameValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username):
            return JsonResponse({'username_exist': 'Username already exists'}, status=409)
        return JsonResponse({'username_valid' : True})


# class EmailValidation(View):
#     def post(self,request):
#         data = json.loads(request.body)
#         email = data['email']
#         if not validate_email(email):
#             return JsonResponse({'email_error': 'Enter Valid Email'}, status=400)
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({'email_exist': 'Email already exists'}, status=409)
#         return JsonResponse({'email_valid' : True})

class EmailValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        try:
            if not validate_email(email):
                return JsonResponse({'email_error': 'Enter Valid Email'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'email_exist': 'Email already exists'}, status=409)
            return JsonResponse({'email_valid' : True})
        except Exception as e:
            return JsonResponse({'email_error': str(e)}, status=500)


class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    def post(self,request):
        # messages.success(request,'Success')
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context  = {
            'fieldvalues' : request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                print(uidb64)
                token = token_generate.make_token(user)
                domain = get_current_site(request).domain
                link = reverse('activate',kwargs={'uidb64':uidb64,'token':token})

                email_subject = 'Activate your account'
                activate_url = 'http://'+domain+link
                email_body = 'Hi'+user.username+'Please use this link to activate your account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@gmail.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account created successfully')
                return render(request, 'authentication/register.html')
            else:
                messages.error(request, 'Email already exists')
        else:
            messages.error(request, 'Username already exists')
        return render(request, 'authentication/register.html')

class VerficationView(View):
    def get(self,request,uidb64,token):
           id = force_str(urlsafe_base64_decode(uidb64))
           user = User.objects.get(pk=id)
           print(user.is_active)

           if not token_generate.check_token(user,token):
                return redirect('login') 
           if user.is_active:
                return redirect('login')
           user.is_active = True
           print('working')
           user.save()
           messages.success(request,'Account activated successfully')
           return redirect('register')

class loginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')
    def post(self,request):
        data = request.POST;
        print(data)
        username = data['username']
        password = data['password']

        if username and password:
            user = auth.authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome, '+user.username+' You are logged in')
                    return redirect('home')
                else:
                    messages.error(request , 'Account is not active, please check your email')
                    return render(request,'authentication/login.html')
            else:
                messages.error(request,'Invalid credentials, try again')
                return render(request,'authentication/login.html')
        else:
            messages.error(request,'Fill all credentials, try again')
            return render(request,'authentication/login.html')
        
class LogOutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You are logged out')
        return redirect('login')