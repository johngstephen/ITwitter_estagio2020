"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .sourceSite import views as source_views
from authentication import views as auth_views

urlpatterns = [
    url(r'^$', source_views.home, name = 'home'),
    url(r'^history/$', source_views.history, name = 'history'),

    url(r'^login/', LoginView.as_view(template_name='register/login.html'), name='login'),
    url(r'^logout/', LogoutView.as_view(template_name='register/logged_out.html', next_page='home'), name='logout'),
    url(r'^password_change_done/', PasswordChangeDoneView.as_view(template_name='register/password_change_done.html'), name='password_change_done'),
    url(r'^password_change/', PasswordChangeView.as_view(template_name='register/password_change_form.html'), name='password_change_form'),
    url(r'^password_reset/done', PasswordResetDoneView.as_view(template_name='register/password_reset_done.html'), name='password_reset_done'),
    url(r'^password_reset/', PasswordResetView.as_view(template_name='register/password_reset_form.html'), name='password_reset_form'),
    url(r'^reset/done', PasswordResetCompleteView.as_view(template_name='register/password_reset_complete.html'), name='password_reset_complete'),
    path(r'^reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='register/password_reset_confirm'
                                                                                    '.html'),
         name='password_reset_confirm'),
    url(r'^create_account', auth_views.register, name='create_user'),
    url(r'^tweets_saved', source_views.tweetSaver, name='tweet_save'),
    url(r'^tweets_removed', source_views.tweetDelete, name='tweet_remove'),


    path('admin/', admin.site.urls),
]
