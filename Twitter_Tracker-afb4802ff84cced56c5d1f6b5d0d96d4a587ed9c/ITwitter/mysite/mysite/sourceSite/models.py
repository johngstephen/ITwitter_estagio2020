# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model

from django.db import models
from idna import unicode

from django.contrib.auth.backends import ModelBackend


# LOGGED_USER = get_user_model()


# class PlatformAccess(models.Model):
#     user = models.ForeignKey(LOGGED_USER, unique=True)
#     password = models.CharField(max_length=64)
#
#     def __str__(self):
#         return "%s" % (unicode(self.user.username))
#
#     def __unicode__(self):
#         return "%s" % (unicode(self.user.username))

# class Utilizador(BaseModel):
#     customer_id = models.CharField(max_length=10)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.TextField()
#     city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
#
#     objects = CustomerManager()
#
#     def __str__(self):
#         return self.customer_id

class Users(models.Model):
    username = models.CharField(max_length=200)
    date_joined = models.DateField()

    def __str__(self):
        return self.username


class FavoriteTweet(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    tweet_id = models.IntegerField()

    def __int__(self):
        return self.tweet_id
