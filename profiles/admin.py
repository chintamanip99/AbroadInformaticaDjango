from django.contrib import admin
from .models import Profile,OTPCache
# Register your models here.
admin.site.register(Profile)
admin.site.register(OTPCache)