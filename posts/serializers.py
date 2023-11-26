from rest_framework import serializers
from .models import Channels,Posts,Comments,Likes
from profiles.models import Profile
from rest_framework.settings import api_settings
from django.contrib.auth.models import User

class PostSearchSerializer(serializers.ModelSerializer):
	class Meta:
		model=Posts
		fields=['id','title']


class UserAbstractSerializer(serializers.ModelSerializer):

	class Meta:
		model=User
		fields=['username','first_name','last_name']

class ProfileSerializer(serializers.ModelSerializer):
	user=UserAbstractSerializer()
	class Meta:
		model=Profile
		fields=['user','image']

class LikesSerializer(serializers.ModelSerializer):
	profile=ProfileSerializer()
	class Meta:
		model=Likes
		exclude=[]

class ChannelSerializer(serializers.ModelSerializer):
	class Meta:
		model=Channels
		fields='__all__'

	def save(self,user123):
		try:
			profile1=Profile.objects.get(user=user123)
			title=self.validated_data['title']
			description=self.validated_data['description']
			channel=Channels.objects.create(
					user=user123,
					title=title,
					description=description,
					)
			if('image' in self.validated_data.keys()):
				image=self.validated_data['image']
				if(image):
					channel.image=image
			channel.save()
			return channel
		except Profile.DoesNotExist:
			raise serializers.ValidationError({'profile_doesnt_exist':'Profile Does Not Exist'})

	def update(self,user123):
		user1=user123
		try:
			channel=Channels.objects.get(user=user1)
			if('image' in self.validated_data.keys()):
				image=self.validated_data['image']
				if(image):
					channel.image=image
			if('title' in self.validated_data.keys()):
				title=self.validated_data['title']
				if(title):
					channel.title=title
			if('description' in self.validated_data.keys()):
				description=self.validated_data['description']
				if(description):
					channel.description=description
			channel.save()
			return channel
		except Channels.DoesNotExist:
			raise serializers.ValidationError({'channel_doesnt_exist':'Channel Does Not Exist'})

class ChannelAbstractSerializer(serializers.ModelSerializer):
	user=UserAbstractSerializer()
	class Meta:
		model=Channels
		fields=['id','user','title','description','image']



class PostsSerializer(serializers.ModelSerializer):
	channel=ChannelAbstractSerializer(required=False)

	class Meta:
		model=Posts
		exclude=[]

	def save(self,user123):
		title=None
		description=None
		post=None
		try:
			channel=Channels.objects.get(user=user123)
			if(not channel.is_granted):
				raise serializers.ValidationError({'channel_doesnt_have_grant_to_add_a_post':'Channel doesnt have grant to add a post'})
		except Channels.DoesNotExist:
			raise serializers.ValidationError({'channel_doesnt_exist':'You have to create a channel to add a post'})
		user1=user123
		if('title' in self.validated_data.keys() and 'description' in self.validated_data.keys()):
			title=self.validated_data['title']
			description=self.validated_data['description']
			if(title!=None and description!=None and len(title)!=0 and len(description)!=0):
				post=Posts.objects.create(
					channel=Channels.objects.get(user=user1),
					title=title,
					description=description,
					)

				if('main_content_text' in self.validated_data.keys()):
					if(self.validated_data['main_content_text'] is not None):
						post.main_content_text=self.validated_data['main_content_text']

				if('main_content_audio' in self.validated_data.keys()):
					if(self.validated_data['main_content_audio'] is not None):
						post.main_content_audio=self.validated_data['main_content_audio']

				if('main_content_image' in self.validated_data.keys()):
					if(self.validated_data['main_content_image'] is not None):
						post.main_content_image=self.validated_data['main_content_image']

				if('main_content_gif' in self.validated_data.keys()):
					if(self.validated_data['main_content_gif'] is not None):
						post.main_content_gif=self.validated_data['main_content_gif']

				if('main_content_video' in self.validated_data.keys()):
					if(self.validated_data['main_content_video'] is not None):
						post.main_content_video=self.validated_data['main_content_video']

				if('main_content_text_link' in self.validated_data.keys()):
					if(self.validated_data['main_content_text_link'] is not None):
						post.main_content_text_link=self.validated_data['main_content_text_link']

				if('main_content_audio_link' in self.validated_data.keys()):
					if(self.validated_data['main_content_audio_link'] is not None):
						post.main_content_audio_link=self.validated_data['main_content_audio_link']

				if('main_content_image_link' in self.validated_data.keys()):
					if(self.validated_data['main_content_image_link'] is not None):
						post.main_content_image_link=self.validated_data['main_content_image_link']

				if('main_content_gif_link' in self.validated_data.keys()):
					if(self.validated_data['main_content_gif_link'] is not None):
						post.main_content_gif_link=self.validated_data['main_content_gif_link']

				if('main_content_video_link' in self.validated_data.keys()):
					if(self.validated_data['main_content_video_link']):
						post.main_content_video_link=self.validated_data['main_content_video_link']
			else:
				raise serializers.ValidationError({'title_description':'Title or Description cant be empty'})
		else:
			raise serializers.ValidationError({'title_description':'Title and Description fields are mandatory'})
		post.save()
		return post

class CommentsSerializer(serializers.ModelSerializer):
	profile=ProfileSerializer(required=False)
	post=PostsSerializer(required=False)
	class Meta:
		model=Comments
		fields='__all__'

	def save(self,user123,post1):
		profile1=Profile.objects.get(user=user123)
		post=post1
		if('comment' in self.validated_data.keys()):
			comment_field=self.validated_data['comment']
			comment=Comments.objects.create(
				profile=profile1,
				post=post,
				comment=comment_field
				)
			post1.no_of_comments+=1
			post1.save()
			comment.save()
			return comment
		else:
			raise serializers.ValidationError({'comment_field_is_mandatory':'Comment field is mandatory'})