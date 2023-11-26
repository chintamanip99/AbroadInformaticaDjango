from django.db import models
from django.utils.timezone import now,localtime
from django.conf import settings
from django.core.validators import FileExtensionValidator
import datetime
from profiles.models import Profile

# Create your models here.
class Category1(models.Model):
	title=models.CharField(max_length=50,null=True,blank=False)
	description=models.TextField(max_length=500,null=True,blank=True)
	image=models.FileField(null=True,blank=True)
	def __str__(self):
		return self.title

class Category2(models.Model):
	category1=models.ForeignKey(Category1,on_delete=models.CASCADE,null=True,blank=False)
	title=models.CharField(max_length=50,null=True,blank=False)
	description=models.TextField(max_length=500,null=True,blank=True)
	image=models.FileField(null=True,blank=True)
	def __str__(self):
		return self.title+"-"+self.category1.title

class Record(models.Model):
	category1=models.ForeignKey(Category1,on_delete=models.CASCADE,null=True,blank=True)
	category2=models.ForeignKey(Category2,on_delete=models.CASCADE,null=True,blank=True)
	title=models.CharField(max_length=50,null=True,blank=False)
	description=models.TextField(max_length=500,null=True,blank=False)
	image=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
	audio=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['mp3','wav','mp4','m4a','wma'])])
	video=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['mp4', 'm4a', 'm4v', 'f4v', 'f4a', 'm4b', 'm4r', 'f4b', 'mov'])])
	text_content=models.FileField(null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['txt','docx'])])
	image_link=models.URLField(max_length=200,null=True,blank=True)
	audio_link=models.URLField(max_length=200,null=True,blank=True)
	video_link=models.URLField(max_length=200,null=True,blank=True)
	text_content_link=models.URLField(max_length=200,null=True,blank=True)
	no_of_likes=models.IntegerField(null=False,default=0,blank=False)
	no_of_shares=models.IntegerField(null=False,default=0,blank=False)
	no_of_comments=models.IntegerField(null=False,default=0,blank=False)
	no_of_reports=models.IntegerField(null=False,default=0,blank=False)
	record_created_date_time = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None),auto_now=False, auto_now_add=False,null=True)
	def __str__(self):
		return self.title
	class Meta:
		ordering = ['-record_created_date_time']

class RecordLikes(models.Model):
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False)
	record=models.ForeignKey(Record,on_delete=models.CASCADE,blank=False)
	class Meta:
		unique_together = ('profile', 'record')
	def __str__(self):
		return self.profile.user.username

class RecordComments(models.Model):
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False)
	record=models.ForeignKey(Record,on_delete=models.CASCADE,blank=False)
	comment=models.TextField(max_length=1000,null=True,blank=False)
	no_of_reports=models.IntegerField(null=True,default=0,blank=False)
	comment_created_date_time = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None),auto_now=False, auto_now_add=False,null=True,blank=False)

	def __str__(self):
		return self.profile.user.username+" id: "+str(self.id)

	class Meta:
		ordering = ['-comment_created_date_time']