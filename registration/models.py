from django.db import models


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
