from enum import unique
from pyexpat import model
from turtle import back
from django.db import models
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

# Create your models here.


class RegisteredUsers(models.Model):
    email = models.EmailField(unique=True, blank=False,
                              max_length=250, null=False)
    password = models.CharField(max_length=20, blank=False, null=False)
    firstname = models.CharField(
         null=False, blank=False, max_length=250)
    lastname = models.CharField(
         null=False, blank=False, max_length=250)

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "registered_users_db"
