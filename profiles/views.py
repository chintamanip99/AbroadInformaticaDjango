from django.shortcuts import render
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer,ProfileSerializer,ProfileSerializer1
from .models import OTPCache
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.timezone import now,localtime
import datetime
import random
from django.core.mail import send_mail,BadHeaderError
from .models import Profile,OTPCache
from rest_framework.permissions import BasePermission
from datetime import timedelta
# Create your views here.
class IsThisUserAdmin(BasePermission):
    message = "You dont have permission to clear cache as you are'nt Superuser"
    def has_permission(self, request, view):
        return request.user.is_superuser

@api_view(['GET'])
@permission_classes([IsThisUserAdmin])
def clear_otp_cache(request):
    print(request.user)
    time_threshold=datetime.datetime.now()-datetime.timedelta(seconds=900)
    print('tt',time_threshold)
    otp_cache=OTPCache.objects.filter(time_when_otp_sent__lt=time_threshold)
    counti=otp_cache.count()
    otp_cache.delete()
    print(otp_cache.count(),"OTPCaches deleted")
    return Response({'no_of_otp_cache_deleted':counti})

@api_view(['POST','GET','PUT'])
@permission_classes([])
def register_user(request):

    if request.method=='POST':
        serializer=UserSerializer(data=request.data)
        data={}
        if(serializer.is_valid()):
            profile=serializer.save()
            data['username']=profile.user.username
            data['email']=profile.user.email
            data['password']=profile.user.password
            token=Token.objects.get(user=profile.user).key
            data['token']=token
        else:
            data=serializer.errors
        return Response(data)

    if request.method=='GET':
        profile=Profile.objects.get(user=request.user)
        return Response({
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            'phone_number':profile.phone_number,
            'image':profile.image.url,
            'is_phone_number_verified':profile.is_phone_number_verified,
            'is_email_verified':profile.is_email_verified,
            'date_joined':request.user.date_joined,
            })
    
    if request.method=='PUT':
        serializer=ProfileSerializer(data=request.data)
        data={}
        if(serializer.is_valid()):
            profile=serializer.update(request.user)
            return Response({
                'profile_updated':'Profile Updated Successfully',
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'email':request.user.email,
                'phone_number':profile.phone_number,
                'image':profile.image.url,
                'is_phone_number_verified':profile.is_phone_number_verified,
                'is_email_verified':profile.is_email_verified,
                'date_joined':request.user.date_joined,
                })
        else:
            return Response(serializer.errors)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def verify_otp(request):

    if request.method=='POST':
        if(not Profile.objects.get(user=request.user).is_email_verified):
            otp_cache=None
            otp=request.data['otp']
            try:
                otp_cache=OTPCache.objects.get(profile__user=request.user)
                print("Now:",datetime.datetime.now())
                print((datetime.datetime.now()-otp_cache.time_when_otp_sent.replace(tzinfo=None)).seconds)
                if(not (datetime.datetime.now()-otp_cache.time_when_otp_sent.replace(tzinfo=None)).seconds>900):
                    print(otp,otp_cache.otp)
                    if(int(otp)==otp_cache.otp):
                        try:
                            profile=Profile.objects.get(user=request.user)
                            profile.is_email_verified=True
                            profile.save()
                            otp_cache.delete()
                            return Response({"email_verified":"Email Verified Successfully!!"})
                        except Profile.DoesNotExist:
                            return Response({"profile_doesnt_exist":"Profile Doesnt Exist"})
                        else:
                            return Response({"worong_otp":"OTP Entered is Wrong,Resend please click on Resend the OTP"})
                else:
                    return Response({"otp_expired":"OTP has expired , Click on Resend OTP"})
            except OTPCache.DoesNotExist:
                return Response({"otp_does_not_exist":"OTP doesnt exist"})
        else:
            return Response({"email_already_verified":"Email is Already Verified"})

    if request.method=='GET':
        try:
            profile=Profile.objects.get(user=request.user)
            otp_cache=OTPCache.objects.get(profile__user=request.user)
            otp_cache.otp=random.randint(100000, 999999)
            otp_cache.time_when_otp_sent=datetime.datetime.now().replace(tzinfo=None)
            otp_cache.save()
            if(request.user.email):
                if(not profile.is_email_verified):
                    try:
                        if(not send_mail('OTP Notofication from BhagwaPataka',"OTP :"+str(otp_cache.otp),'cmp151999@gmail.com',[profile.user.email],fail_silently=True)>0):
                            return Response({'otp_failed':'OTP Sending Failed (Zero OTPs send)'})
                        else:
                            return Response({'otp_sent_successfully':'OTP sent successfully'})
                    except BadHeaderError:
                        return Response({'otp_failed':'OTP Sending Failed'})
                else:
                    return Response({"email_already_verified":"Email is Already Verified"})
            else:
                return Response({"email_not_present":"Email field is not filled"})
        except OTPCache.DoesNotExist:
            profile=Profile.objects.get(user=request.user)
            otp_cache=OTPCache.objects.create(
                profile=profile
                )
            otp_cache.otp=random.randint(100000, 999999)
            otp_cache.time_when_otp_sent=datetime.datetime.now().replace(tzinfo=None)
            otp_cache.save()
            if(profile.user.email):
                if(not profile.is_email_verified):
                    try:
                        if(not send_mail('OTP Notofication from BhagwaPataka',"OTP :"+str(otp_cache.otp),'cmp151999@gmail.com',[profile.user.email],fail_silently=True)>0):
                            return Response({'otp_failed':'OTP Sending Failed (Zero OTPs send)'})
                        else:
                            return Response({'otp_sent':'OTP Sent Successfully'})
                    except BadHeaderError:
                        return Response({'otp_failed':'OTP Sending Failed'})
                else:
                    return Response({'email_already_verified':'Email Already Verified'})
            else:
                return Response({"email_not_present":"Email field is not filled"})





    # if request.method=='GET':
    #     try:
    #         profile=Profile.objects.get(user=request.user)
    #         try:
    #             otp_cache=OTPCache.objects.get(profile=profile)
    #             otp_cache.otp=random.randint(100000, 999999)
    #             otp_cache.time_when_otp_sent=datetime.datetime.now().replace(tzinfo=None)
    #             otp_cache.save()
    #             if(profile.user.email):
    #                 if(not profile.is_email_verified):
    #                     try:
    #                         if(not send_mail('OTP Notofication from BhagwaPataka',"OTP :"+str(otp_cache.otp),'cmp151999@gmail.com',[profile.user.email],fail_silently=True)>0):
    #                             return Response({'otp_failed':'OTP Sending Failed (Zero OTPs send)'})
    #                     except BadHeaderError:
    #                         return Response({'otp_failed':'OTP Sending Failed'})
    #                 else:
    #                     return Response({"email_already_verified":"Email is Already Verified"})
    #             else:
    #                 return Response({"email_not_present_in_profile":"Please enter email in profile"})
    #         except OTPCache.DoesNotExist:
    #             otp_cache=OTPCache.objects.create(
    #                 profile=profile
    #                 )
    #             try:
    #                 if(not send_mail('OTP Notofication from BhagwaPataka',"OTP :"+str(otp_cache.otp),'cmp151999@gmail.com',[profile.user.email],fail_silently=True)>0):
    #                     return Response({'otp_failed':'OTP Sending Failed (Zero OTPs send)'})
    #                 else:
    #                     return Response({'otp_sent_successfully':'OTP sent successfully'})
    #             except BadHeaderError:
    #                 return Response({'otp_failed':'OTP Sending Failed'})
    #             otp_cache.save()
    #             return Response({'otp_sent':'OTP Sent Successfully'})
    #             if(profile.user.email):
    #                 try:
    #                     if(not send_mail('OTP Notofication from BhagwaPataka',"OTP :"+str(otp_cache.otp),'cmp151999@gmail.com',[profile.user.email],fail_silently=True)>0):
    #                         return Response({'otp_failed':'OTP Sending Failed (Zero OTPs send)'})
    #                     else:
    #                         return Response({'otp_sent':'OTP Sent Successfully'})
    #                 except BadHeaderError:
    #                     return Response({'otp_failed':'OTP Sending Failed'})
    #             else:
    #                 return Response({'enter_email_in_profile':'PLease fill the email field in profile'})
    #     except Profile.DoesNotExist:
    #         return Response({"profile_cache_doesnt_exist":"Profile doesnt exist"})