from django.urls import path, include
from accounts.views import logout, login, registration 

urlpatterns = [
    path("logout/", logout, name="logout"),
    path("login/", login, name="login"),
    path("register/", registration, name="registration"),
 
   # path("password-reset/", include("django.contrib.auth.urls")),
]
