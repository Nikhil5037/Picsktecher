
from django.contrib import admin
from django.urls import path
from registration import views as registration
from uploadImage import views as uploadimg
from django.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include('rest_framework.urls')),
    path("register/", registration.Register.as_view()),
    path("login/", registration.Login.as_view()),
    path("upload/",uploadimg.UploadImage.as_view())
]
