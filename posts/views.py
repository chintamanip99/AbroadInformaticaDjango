from django.shortcuts import render
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Channels,Likes,Posts,Comments
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .serializers import LikesSerializer,PostSearchSerializer
from .serializers import ChannelSerializer,PostsSerializer,CommentsSerializer,ChannelAbstractSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from profiles.models import Profile
from rest_framework.permissions import BasePermission
from BhagwaPataka.urls import IsConfirmedEmail

class PaginationForSearch(PageNumberPagination,APIView):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class StandardResultsSetPaginationForChannels(PageNumberPagination,APIView):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000

class StandardResultsSetPagination(PageNumberPagination,APIView):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get(self,request,n):
    	self.page_size=n
    	PageNumberPagination.page_size = n
    	return Response({'successfully_changed_page_size':'Successfully Changed Page Size'+str(PageNumberPagination.page_size)})

class Channel(generics.ListAPIView):
	permission_classes = [(IsConfirmedEmail)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)
	pagination_class=StandardResultsSetPaginationForChannels
	queryset=Channels.objects.all()
	serializer_class=ChannelAbstractSerializer
	filter_backends = [filters.SearchFilter,filters.OrderingFilter]
	search_fields  = ['title', 'description','user__username','user__first_name','user__last_name']

	def post(self, request,type):
		if(type==0):
			try:
				channel11=Channels.objects.get(user=request.user)
				c11=ChannelSerializer(channel11)
				return Response({'channel_exists':'Channel Already Exists','channel_data':c11.data})
			except Channels.DoesNotExist:
				c=ChannelSerializer(data=request.data)
				if(c.is_valid()):
					channel=c.save(request.user)
					data={}
					data.update({'username':channel.user.username,'channel_title':channel.title,'channel_description':channel.description})
					if(channel.image):
						data['image']=channel.image.url
					data['channel_created']="Channel Created Successfully!,You can add Posts!"
					return Response(data)
				else:
					return Response({'invalid_input_data':c.errors})
		if(type==1):
			c=ChannelSerializer(data=request.data)
			if(c.is_valid()):
				channel=c.update(request.user)
				data={}
				data.update({'username':channel.user.username,'channel_title':channel.title,'channel_description':channel.description})
				if(channel.image):
					data['image']=channel.image.url
				data['channel_created']="Channel Updated Successfully!!"
				return Response(data)
			return Response({'invalid_input_data':c.errors})

	def put(self, request,type):
		try:
			channel=Channels.objects.get(user=request.user)
			serializer=ChannelSerializer(channel)
			return Response(serializer.data)
		except Channels.DoesNotExist:
			return Response({'channel_doesnt_exist':'Channel doesnt exist'})

	def delete(self, request,id,type):
		try:
			channel=Channels.objects.get(user=request.user,id=id)
			channel.delete()
			return Response({'channel_deleted':'Channel Deleted Successfully'})
		except Channels.DoesNotExist:
			return Response({'channel_doesnt_exist':'Channel Does Not Exist'})

class PostSearch(generics.ListAPIView):
	permission_classes = [(IsConfirmedEmail)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)
	pagination_class=PaginationForSearch
	queryset=Posts.objects.all()
	serializer_class=PostSearchSerializer
	filter_backends = [filters.SearchFilter,filters.OrderingFilter]
	search_fields  = ['title']

class Comment(APIView):
	permission_classes = [(IsConfirmedEmail)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)

	def post(self, request,id):
		try:
			post=Posts.objects.get(id=id)
			c=CommentsSerializer(data=request.data)
			if(c.is_valid()):
				comment=c.save(user123=request.user,post1=post)
				data={}
				data.update({'username':comment.profile.user.username,'post_title':comment.post.title,'comment':comment.comment,'no_of_comments':comment.post.no_of_comments})
				return Response(data)
			else:
				return Response({'invalid_input_data':c.errors})
		except Posts.DoesNotExist:
			return Response({'post_doesnt_exist':'Post Doesnt Exist'})

	def get(self, request,id):
		post=None
		try:
			post=Posts.objects.get(id=id)
			if(post.no_of_comments>0):
				comments=Comments.objects.filter(post=post)
				if(len(comments)>0):
					c=CommentsSerializer(comments,many=True)
					return Response({'comments':c.data})
				else:
					return Response({'no_comments':'Comments do not exist'})
			else:
				return Response({'no_comments':'Comments do not exist'})
		except Posts.DoesNotExist:
			return Response({'post_doesnt_exist':'Post Doesnt Exist'})

	def delete(self, request,id):
		try:
			comment=Comments.objects.get(user=request.user,id=id)
			if(comment.profile.user==request.user):
				post=comment.post
				post.no_of_comments-=1
				post.save()
				comment.delete()
				return Response({'comment_deleted':'Comment deleted successfully'})
			else:
				return Response({'cant_delete_comment':'You cant delete this comment as you have not created it'}) 
		except Comments.DoesNotExist:
			return Response({'comment_doesnt_exist':'Comment Doesnt Exist'})

class Post(generics.ListAPIView):
	permission_classes = [(IsConfirmedEmail)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)
	pagination_class=StandardResultsSetPagination
	queryset=Posts.objects.filter(channel__is_granted=True)
	serializer_class=PostsSerializer
	filter_backends = [filters.SearchFilter]
	search_fields  = ['title', 'description','channel__title','channel__user__username','channel__user__first_name','channel__user__last_name']

	print('page size ',StandardResultsSetPagination.page_size)

	def post(self, request,id):
		serializer=PostsSerializer(data=request.data)
		if(serializer.is_valid()):
			post=serializer.save(request.user)
			serializer=PostsSerializer(post)
			return Response({'post_data':serializer.data,'post_created_success':'Post Created Successfully'})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request,id):
		try:
			post=Posts.objects.get(channel=Channels.objects.get(user=request.user),id=id)
			post.delete()
			return Response({'post_deleted':'Post Deleted Successfully'})
		except Posts.DoesNotExist:
			return Response({'post_doesnt_exist':'Post Does Not Exist'})

	def put(self,request,id):
		try:
			post=Posts.objects.get(id=id)
			serializer=PostsSerializer(post)
			return Response({'results':[serializer.data]})
		except Posts.DoesNotExist:
			return Response({'results':[]})

class Like(APIView):
	permission_classes = [(IsConfirmedEmail)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)

	def put(self,request,id):
		likes=Likes.objects.filter(post__id=id)
		if(len(likes)>0):
			serializer=LikesSerializer(likes,many=True)
			return Response(serializer.data)
		else:
			return Response({'no_likes':'No likes for this post till now'})

	def post(self, request,id):
		try:
			post=Posts.objects.get(id=id)
			profile=Profile.objects.get(user=request.user)
			try:
				like=Likes.objects.get(profile=profile,post=post)
				post=like.post
				post.no_of_likes-=1
				post.save()
				like.delete()
				return Response({'post_unliked_successfully':'Post Unliked successfully','no_of_likes':post.no_of_likes})
			except Likes.DoesNotExist:
				like=Likes.objects.create(profile=profile,post=post)
				post.no_of_likes+=1
				post.save()
				like.save()
				return Response({'post_liked_successfully':'Post liked successfully','no_of_likes':post.no_of_likes})
		except Posts.DoesNotExist:
			return Response({'post_doesnt_exist':'Post Doesnt Exist'})

	def get(self, request,id):
		try:
			post=Posts.objects.get(id=id)
			profile=Profile.objects.get(user=request.user)
			try:
				like=Likes.objects.get(profile=profile,post=post)
				return Response({'like':'exists','no_of_likes':post.no_of_likes})
			except Likes.DoesNotExist:
				return Response({'like':'doesnt_exist'})
		except Posts.DoesNotExist:
			return Response({'post_doesnt_exist':'Post Doesnt Exist'})
			