from django.db import models
from django.conf import settings
from django.utils.timezone import now,localtime
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
import datetime
# from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission



# permission =  GoogleDriveFilePermission(
#    GoogleDrivePermissionRole.READER,
#    GoogleDrivePermissionType.USER,
#    "foo@mailinator.com"
# )

# exposed_request=None
# gd_storage=None

# def RequestExposerMiddleware(get_response):
#     def middleware(request):
#     	global exposed_request,gd_storage
#     	exposed_request = request
#     	response = get_response(request)
#     	if(exposed_request is not None):
#     		print(exposed_request)
#     	if(exposed_request.user.is_authenticated):
#     		print(exposed_request.user.is_authenticated)
#     		gd_storage=GoogleDriveStorage(permissions=(permission,))
#     	return response
#     return middleware

# from .middleware import RequestMiddleware

# # First we need create an instance of that and later get the current_request assigned
# request = RequestMiddleware(get_response=None)
# request = request.thread_local.current_request


# from .middleware import RequestMiddleware

# # First we need create an instance of that and later get the current_request assigned
# request = RequestMiddleware(get_response=None)
# request = request.thread_local.current_request

# gd_storage=GoogleDriveStorage(permissions=(permission,))
class FileValidator(object):
    error_messages = {
     'main_content_image': "Files llof type are not supported.",
    }

# Create your models here.
class Channels(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=False)
	title=models.CharField(max_length=50,null=True,blank=False)
	description=models.TextField(max_length=500,null=True,blank=False)
	image=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
	is_granted=models.BooleanField(default=True,null=True,blank=False)
	channel_created_date_time = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None),auto_now=False, auto_now_add=False,null=True,blank=False)
	def __str__(self):
		return "Channel Name: "+self.title+" User: "+self.user.username

class Posts(models.Model):
	channel=models.ForeignKey(Channels,on_delete=models.CASCADE,null=True,blank=False)
	title=models.CharField(max_length=100,null=True,blank=False)
	description=models.TextField(max_length=65535,null=True,blank=False)
	main_content_text=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['txt','docx'])])
	main_content_audio=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['mp3','wav','mp4','m4a','wma'])])
	main_content_image=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
	main_content_gif=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['gif'])])
	main_content_video=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['mp4', 'm4a', 'm4v', 'f4v', 'f4a', 'm4b', 'm4r', 'f4b', 'mov'])])
	main_content_text_link=models.URLField(max_length=200,null=True,blank=True)
	main_content_audio_link=models.URLField(max_length=200,null=True,blank=True)
	main_content_image_link=models.URLField(max_length=65535,null=True,blank=True)
	main_content_gif_link=models.URLField(max_length=200,null=True,blank=True)
	main_content_video_link=models.URLField(max_length=200,null=True,blank=True)
	no_of_likes=models.IntegerField(null=False,default=0,blank=False)
	no_of_shares=models.IntegerField(null=False,default=0,blank=False)
	no_of_comments=models.IntegerField(null=False,default=0,blank=False)
	no_of_reports=models.IntegerField(null=False,default=0,blank=False)
	post_created_date_time = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None),null=True)
	def __str__(self):
		return self.title+" id ="+str(self.id)
	class Meta:
		ordering = ['-post_created_date_time']

class Likes(models.Model):
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False)
	post=models.ForeignKey(Posts,on_delete=models.CASCADE,blank=False)
	class Meta:
		unique_together = ('profile', 'post')
	def __str__(self):
			return str(self.profile.user.username)+" post: "+str(self.post.title)

class Comments(models.Model):
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False)
	post=models.ForeignKey(Posts,on_delete=models.CASCADE,blank=False)
	comment=models.TextField(max_length=1000,null=True,blank=False)
	no_of_reports=models.IntegerField(null=True,default=0,blank=False)
	comment_created_date_time = models.DateTimeField(default=now,auto_now=False, auto_now_add=False,null=True,blank=False)

	def __str__(self):
			return str(self.profile.user.username)+" post: "+str(self.post.title)