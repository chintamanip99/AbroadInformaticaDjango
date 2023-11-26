from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile,OTPCache
import datetime
import random
import re
from django.core.mail import send_mail,BadHeaderError

class UserSerializer(serializers.ModelSerializer):
	password2=serializers.CharField(write_only=True,required=True)
	age=serializers.CharField(write_only=True,required=True)
	email=serializers.CharField(write_only=True,required=True)
	first_name=serializers.CharField(write_only=True,required=False)
	last_name=serializers.CharField(write_only=True,required=False)
	image=serializers.FileField(write_only=True,required=False)
	class Meta:
		model=User
		fields=['username','email','password','password2','age','image','first_name','last_name']

	def save(self):
		username=self.validated_data['username']
		password=self.validated_data['password']
		password2=self.validated_data['password2']
		email=self.validated_data['email']
		if('image' in self.validated_data.keys()):
			image=self.validated_data['image']
		age=int(self.validated_data['age'])
		regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
		if not re.search(regex,email):
			raise serializers.ValidationError({'email':'Email entered is invalid'})
		if password!=password2:
			raise serializers.ValidationError({'password':'Passwords doesnt match'})
		if age<=0:
			raise serializers.ValidationError({'age':'Age cant be negative or zero'})
		if age<18:
			raise serializers.ValidationError({'age':'You have to be 18 or 18+ to create an account'})			
		else:
			user=User.objects.create_user(
				email=email,
				username=username,
				password=password
			)
			if('first_name' in self.validated_data.keys()):
				user.first_name=self.validated_data['first_name']
			if('last_name' in self.validated_data.keys()):
				user.last_name=self.validated_data['last_name']
			user.save()
			profile=Profile.objects.create(
				user=user,
				age=age
			)
			if('image' in self.validated_data.keys()):
				profile.image=image
			profile.save()
			otp_cache=OTPCache.objects.create(
				profile=profile
				)
			otp_cache.otp=random.randint(100000, 999999)
			otp_cache.time_when_otp_sent=datetime.datetime.now().replace(tzinfo=None)
			otp_cache.save()
			if(profile.user.email):
				try:
					if(not send_mail('OTP Notofication from BhagwaPataka',"OTP :"+str(otp_cache.otp),'cmp151999@gmail.com',[profile.user.email],fail_silently=True)>0):
						raise serializers.ValidationError({'otp_failed':'OTP Sending Failed (Zero OTPs send)'})
				except BadHeaderError:
						raise serializers.ValidationError({'otp_failed':'OTP Sending Failed'})
			return profile
	
	def update(self,user12):
		user=user12
		profile=Profile.objects.get(user=user)
		if('password' in self.validated_data.keys()):
			if('password2' in self.validated_data.keys()):
				password=self.validated_data['password']
				password2=self.validated_data['password']
				if(password==password2):
					user.password=password
				else:
					raise serializers.ValidationError({'passwords_dont_match':'Passwords Donot Match'})
			else:
				raise serializers.ValidationError({'password_password2_not_available':'Password and Confirm Password Are Mandatory'})
		if('image' in self.validated_data.keys()):
			image=self.validated_data['image']
			profile.image=image
		if('email' in self.validated_data.keys()):
			email=self.validated_data['email']
			regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
			if not re.search(regex,email):
				raise serializers.ValidationError({'email':'Email entered is invalid'})
			if(user.email!=email):
				user.email=email
				profile.is_email_verified=False
		if('first_name' in self.validated_data.keys()):
			if(len(self.validated_data['first_name'])>0):
				first_name=self.validated_data['first_name']
				user.first_name=first_name
			else:
				raise serializers.ValidationError({'first_name_blank':'First Name Cant Be Blank'})
		if('last_name' in self.validated_data.keys()):
			if(len(self.validated_data['last_name'])>0):
				last_name=self.validated_data['last_name']
				user.last_name=last_name
			else:
				raise serializers.ValidationError({'last_name_blank':'Last Name Cant Be Blank'})
		profile.save()
		user.save()
		return profile

class UserSerializer1(serializers.ModelSerializer):
	class Meta:
		model=User
		exclude=[]

class ProfileSerializer1(serializers.ModelSerializer):
	user=UserSerializer1()
	class Meta:
		model=Profile
		exclude=[]

class ProfileSerializer(serializers.ModelSerializer):
	password=serializers.CharField(write_only=True,required=False)
	password2=serializers.CharField(write_only=True,required=False)
	email=serializers.CharField(write_only=True,required=False)
	first_name=serializers.CharField(write_only=True,required=False)
	last_name=serializers.CharField(write_only=True,required=False)
	phone_number=serializers.CharField(write_only=True,required=False)
	image=serializers.FileField(write_only=True,required=False)
	user=UserSerializer1(required=False)
	class Meta:
		model=Profile
		fields=['user','image','email','password','password2','first_name','last_name','phone_number']

	def update(self,user12):
		user=user12
		profile=Profile.objects.get(user=user)
		if('password' in self.validated_data.keys()):
			if('password2' in self.validated_data.keys()):
				password=self.validated_data['password']
				password2=self.validated_data['password2']
				if(password!=password2):
					raise serializers.ValidationError({'passwords_dont_match':'Passwords Donot Match'})
				else:
					user.password=password
			else:
				raise serializers.ValidationError({'password_password2_not_available':'Password and Confirm Password Are Mandatory'})
		if('image' in self.validated_data.keys()):
			image=self.validated_data['image']
			profile.image=image
		if('email' in self.validated_data.keys()):
			email=self.validated_data['email']
			regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
			if not re.search(regex,email):
				raise serializers.ValidationError({'email':'Email entered is invalid'})
			if(user.email!=email):
				user.email=email
				profile.is_email_verified=False
		if('first_name' in self.validated_data.keys()):
			if(len(self.validated_data['first_name'])>0):
				first_name=self.validated_data['first_name']
				user.first_name=first_name
			else:
				raise serializers.ValidationError({'first_name_blank':'First Name Cant Be Blank'})
		if('phone_number' in self.validated_data.keys()):
			if(len(self.validated_data['phone_number'])>0):
				phone_number=self.validated_data['phone_number']
				if(profile.phone_number!=phone_number):
					profile.phone_number=phone_number
					profile.is_phone_number_verified=False
			else:
				raise serializers.ValidationError({'phone_number_blank':'Phone Number Cant Be Blank'})
		if('last_name' in self.validated_data.keys()):
			if(len(self.validated_data['last_name'])>0):
				last_name=self.validated_data['last_name']
				user.last_name=last_name
			else:
				raise serializers.ValidationError({'last_name_blank':'Last Name Cant Be Blank'})
		profile.save()
		user.save()
		return profile