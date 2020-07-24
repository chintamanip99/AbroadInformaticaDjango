"""AbroadInformatica URL Configuration

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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.permissions import BasePermission
from profiles.models import Profile

# from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission
from rest_framework.authtoken.models import Token


# permission =  GoogleDriveFilePermission(
#    GoogleDrivePermissionRole.READER,
#    GoogleDrivePermissionType.USER,
#    "foo@mailinator.com"
# )

class IsConfirmedEmail(BasePermission):
    # message = "Email/Phone No. is not verified"
    message={}
    def has_permission(self, request, view):
        if(request.user.is_authenticated):
            if(request.user.is_superuser):
                return True
            else:
                try:
                    profile=Profile.objects.get(user=request.user)
                    if(profile.user.email is not None or profile.phone_number is not None):
                        if(profile.is_email_verified or profile.is_phone_number_verified):
                            return True
                        else:
                            self.message['unverified']="Email/Phone No. is not verified,Click on Resend OTP to verify email/Phone Number"
                            return False
                    else:
                        # self.message="One of Fields Email or Phone Number Should be filled"
                        self.message['empty_fields']="One of Fields Email or Phone Number Should be filled,Update your profile and fill in your Email/Phone Number"
                        return False
                except Profile.DoesNotExist:
                    return False
        else:
            return False

@api_view(['GET'])
@permission_classes([])
def protected_serve(request, path, document_root=None, show_indexes=False):
    path=path.split("&Token=")
    if(len(path)>1):
        try:
            token=Token.objects.get(key=path[1])
            return serve(request, path[0], document_root, show_indexes)
        except Token.DoesNotExist:
            return Response({'authentication':'Authentication Credentials not provided/ Wrong Credentials'})
    else:
        return Response({'authentication':'Token should be provided with URL'})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include("profiles.urls","profiles")),
    path('content/', include("content.urls","content")),
    path('posts/', include("posts.urls","posts")),
]

# if(request.user.is_superuser):
#     print('superuser')
# gd_storage=GoogleDriveStorage(permissions=(permission,))
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,protected_serve,document_root=settings.MEDIA_ROOT)