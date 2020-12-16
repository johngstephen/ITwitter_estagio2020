from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from . import forms
from django.contrib.auth.models import User
from mysite.sourceSite.models import Users
import datetime


def register(request):
    if request.method == 'POST':
        register_form = forms.CreateAccountForm(request.POST)
        if register_form.is_valid():
            user_first_name = register_form.cleaned_data.get('user_first_name')
            user_last_name = register_form.cleaned_data.get('user_last_name')
            username = register_form.cleaned_data.get('username')
            user_password = register_form.cleaned_data.get('user_password')
            user_email = register_form.cleaned_data.get('user_email')

            user = User.objects.create_user(username, user_email, user_password)
            favorites_user = Users(username=user_email, date_joined=datetime.date.today())
            favorites_user.save()
            user.first_name= user_first_name
            user.last_name = user_last_name
            user.save()

            return render(request, 'register/registry_done.html')
    else:
        register_form = forms.CreateAccountForm()
    return render(request, 'register/create_account.html', {'create_account_form': register_form})
