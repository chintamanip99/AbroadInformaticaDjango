from django.shortcuts import render
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.
import schedule
from rest_framework import generics
from rest_framework import filters
from posts.views import StandardResultsSetPagination
import time
from .models import Category1,Category2,Record,RecordLikes,RecordComments
from .serializers import (Category1AbstractSerializer,
	RecordLikesSerializer,
	Category2AbstractSerializer,
	RecordAbstractSerializer,
	Category1DetailSerializer,
	Category2DetailSerializer,
	RecordCommentsSerializer,
	RecordDetailSerializer)

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from BhagwaPataka.urls import IsConfirmedEmail
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from twilio.rest import Client 
import time
from profiles.models import Profile
from posts.models import Channels
from posts.serializers import ChannelAbstractSerializer


@api_view(['GET'])
@permission_classes([])
def twilio(request):
	account_sid = 'AC4dc42d945d580e0b3f13b7f33141a0b0' 
	auth_token = '6002dd65e7b1327abe869654ae1539c8' 
	client = Client(account_sid, auth_token) 
	list1=['+919834632388','+919284356619']
	for j in range(4):
		for i in list1:
			message = client.messages.create( 
				from_='whatsapp:+14155238886',
				body='pooja bindok',
				to='whatsapp:'+i 
				)
			time.sleep(10)
	return Response({"sent":"watsaopmessagw sent"})

@api_view(['GET'])
@permission_classes([])
def get_server_ip_address(request):
	return Response({"ip":"192.168.29.221","port":"8000"})

class Content(generics.ListAPIView):
	permission_classes = []
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)
	pagination_class=StandardResultsSetPagination
	queryset=Record.objects.all()
	serializer_class=RecordDetailSerializer
	filter_backends = [filters.SearchFilter]

@api_view(['GET'])
@permission_classes([])
def show_full_content(request,hierarchy_level,category_id):
	if request.method == 'GET':
		data={}
		print(request.user)

		if(hierarchy_level==0):
			category1=Category1.objects.all()
			serializer=Category1AbstractSerializer(category1,many=True)
			data['Category1']=serializer.data

			records=Record.objects.filter(category1__isnull=True,category2__isnull=True)
			serializer=RecordAbstractSerializer(records,many=True)
			data['Records']=serializer.data

		if(hierarchy_level==1):
			category2=Category2.objects.filter(category1__id=category_id)
			serializer=Category2AbstractSerializer(category2,many=True)
			data['Category2']=serializer.data

			records=Record.objects.filter(category1__id=category_id)
			serializer=RecordAbstractSerializer(records,many=True)
			data['Records']=serializer.data

		if(hierarchy_level==2):
			records=Record.objects.filter(category2__id=category_id)
			serializer=RecordAbstractSerializer(records,many=True)
			data['Records']=serializer.data

		if(hierarchy_level==3):
			records=Record.objects.all()
			serializer=RecordAbstractSerializer(records,many=True)
			data['Records']=serializer.data

		return Response(data)

@api_view(['GET'])
@permission_classes([])
def show_details_of_content(request,type,id):
	if request.method == 'GET':
		data={}
		print(request.user)
		if(type==3):
			try:
				record=Record.objects.get(id=id)
				serializer=RecordDetailSerializer(record)
				data['next']=""
				data['previous']=""
				data['results']=[serializer.data]
			except Records.DoesNotExist:
				data['record_doesnt_exist']='Record Doest Not Exist'

		if(type==1):
			try:
				category1=Category1.objects.get(id=id)
				serializer=Category1DetailSerializer(category1)
				data['next']=""
				data['previous']=""
				data['results']=[serializer.data]
			except Category1.DoesNotExist:
				data['category1_doesnt_exist']='Category1 Doest Not Exist'

		if(type==2):
			try:
				category2=Category2.objects.get(id=id)
				serializer=Category2DetailSerializer(category2)
				data['next']=""
				data['previous']=""
				data['results']=[serializer.data]
			except Category2.DoesNotExist:
				data['category2_doesnt_exist']='Category2 Doest Not Exist'

		if(type==4):
			try:
				channel=Channels.objects.get(id=id)
				serializer=ChannelAbstractSerializer(channel)
				data['next']=""
				data['previous']=""
				data['results']=[serializer.data]
			except Channels.DoesNotExist:
				data['channel_doesnt_exist']='Channel Doest Not Exist'

		return Response(data)

class RecordLike(APIView):
	permission_classes = [(IsConfirmedEmail)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)

	def put(self,request,id):
		likes=RecordLikes.objects.filter(record__id=id)
		if(len(likes)>0):
			serializer=RecordLikesSerializer(likes,many=True)
			return Response(serializer.data)
		else:
			return Response({'no_likes':'No likes for this content till now'})


	def get(self, request,id):
		try:
			record=Record.objects.get(id=id)
			profile=Profile.objects.get(user=request.user)
			try:
				recordlike=RecordLikes.objects.get(profile=profile,record=record)
				return Response({'like':'exists','no_of_likes':record.no_of_likes})
			except RecordLikes.DoesNotExist:
				return Response({'like':'doesnt_exist'})
		except Record.DoesNotExist:
			return Response({'post_doesnt_exist':'Content Doesnt Exist'})

	def post(self, request,id):
		try:
			record=Record.objects.get(id=id)
			try:
				like=RecordLikes.objects.get(profile__user=request.user,record=record)
				record=like.record
				record.no_of_likes-=1
				record.save()
				like.delete()
				return Response({'record_unliked_successfully':'Record Unliked successfully','no_of_likes':record.no_of_likes})
			except RecordLikes.DoesNotExist:
				like=RecordLikes.objects.create(profile=Profile.objects.get(user=request.user),record=record)
				record.no_of_likes+=1
				record.save()
				like.save()
				return Response({'record_liked_successfully':'Record liked successfully','no_of_likes':record.no_of_likes})
		except Record.DoesNotExist:
			return Response({'record_doesnt_exist':'Record Doesnt Exist'})

class RecordComment(APIView):
	permission_classes = [(IsConfirmedEmail)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)

	def post(self, request,id):
		try:
			record=Record.objects.get(id=id)
			c=RecordCommentsSerializer(data=request.data)
			if(c.is_valid()):
				comment=c.save(user123=request.user,record1=record)
				data={}
				data.update({'username':comment.profile.user.username,'post_title':comment.record.title,'comment':comment.comment,'no_of_comments':comment.record.no_of_comments})
				return Response(data)
			else:
				return Response({'invalid_input_data':c.errors})
		except Record.DoesNotExist:
			return Response({'record_doesnt_exist':'Record Doesnt Exist'})

	def get(self, request,id):
		record=None
		try:
			record=Record.objects.get(id=id)
			if(record.no_of_comments>0):
				comments=RecordComments.objects.filter(record=record)
				if(len(comments)>0):
					c=RecordCommentsSerializer(comments,many=True)
					return Response({'comments':c.data})
				else:
					return Response({'no_comments':'Comments do not exist'})
			else:
				return Response({'no_comments':'Comments do not exist'})
		except Record.DoesNotExist:
			return Response({'record_doesnt_exist':'Record Doesnt Exist'})

	def delete(self, request,id):
		try:
			comment=RecordComments.objects.get(profile__user=request.user,id=id)
			if(comment.profile.user==request.user):
				record=comment.record
				record.no_of_comments-=1
				record.save()
				comment.delete()
				return Response({'comment_deleted':'Comment deleted successfully'})
			else:
				return Response({'cant_delete_comment':'You cant delete this comment as you have not created it'}) 
		except RecordComments.DoesNotExist:
			return Response({'comment_doesnt_exist':'Comment Doesnt Exist'})


