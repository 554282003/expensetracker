from django.shortcuts import render
import os
import json
from django.conf import settings
import pdb
from .models import UserPreference
from django.contrib import messages

def index(request):
    exists = UserPreference.objects.filter(user=request.user).exists()
    print(exists,"user")
    user_preferences = None

    if exists:
        user_preferences =  UserPreference.objects.get(user=request.user)
        print(user_preferences)

    currency_data = []  # Declare currency_data outside the if statement
    
    if request.method == 'GET':
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                currency_data.append({'key': k, 'value': v})
    
        return render(request, 'preferences/index.html', {'currencies': currency_data,'user_preferences':user_preferences})
    else:
        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
            messages.success(request, 'Changes Saved')
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, 'Changes Saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data , 'user_preferences':user_preferences})
