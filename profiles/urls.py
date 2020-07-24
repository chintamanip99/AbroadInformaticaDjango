from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from profiles.views import clear_otp_cache,register_user,verify_otp

app_name="profiles"
urlpatterns = [
    path("login_user/",obtain_auth_token,name="obtain_auth_token"),
    path("register_user/",register_user,name="register_user"),
    path("clear_otp_cache/",clear_otp_cache,name="clear_otp_cache"),
    path("verify_otp/",verify_otp,name="verify_otp")
]