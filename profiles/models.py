from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now,localtime
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import FileExtensionValidator
import random
import datetime

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=False)
	phone_number=models.CharField(max_length=20,null=True,blank=True)
	age=models.PositiveIntegerField(default=21, blank=False,validators=[MinValueValidator(18), MaxValueValidator(100)],null=False)
	image=models.FileField(null=True,blank=True,upload_to=settings.MEDIA_ROOT+"/Profiles",validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
	is_phone_number_verified=models.BooleanField(default=False,null=True,blank=False)
	is_email_verified=models.BooleanField(default=False,null=True,blank=False)
	is_regular=models.BooleanField(default=False,null=True,blank=False)
	no_of_times_app_started=models.IntegerField(default=0,null=True,blank=False)
	account_created_date = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None),auto_now=False, auto_now_add=False,null=True,blank=False)
	def __str__(self):
		return self.user.username

class OTPCache(models.Model):
	profile=models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=False)
	otp=models.IntegerField(default=random.randint(100000, 999999),null=True,blank=False)
	time_when_otp_sent=models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None),auto_now=False, auto_now_add=False,null=True,blank=False)
	def __str__(self):
		return "username: "+self.profile.user.username+" otp:"+str(self.otp)+" time:"+str(self.time_when_otp_sent)

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance)