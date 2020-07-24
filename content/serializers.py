from rest_framework import serializers
from .models import Category1,Category2,Record,RecordLikes,RecordComments
from posts.serializers import UserAbstractSerializer,ProfileSerializer
from profiles.models import Profile



class Category1AbstractSerializer(serializers.ModelSerializer):
	class Meta:
		model=Category1
		fields=['id','title','image']

class Category2AbstractSerializer(serializers.ModelSerializer):
	category1=Category1AbstractSerializer()
	class Meta:
		model=Category2
		fields=['id','title','category1','image']

class RecordAbstractSerializer(serializers.ModelSerializer):
	category1=Category1AbstractSerializer()
	category2=Category2AbstractSerializer()
	class Meta:
		model = Record
		fields = ['id','title','category1','category2']

class Category1DetailSerializer(serializers.ModelSerializer):
	class Meta:
		model=Category1
		fields=['id','title','description','image']

class Category2DetailSerializer(serializers.ModelSerializer):
	category1=Category1AbstractSerializer()
	class Meta:
		model=Category2
		fields=['id','title','category1','description','image']

class RecordDetailSerializer(serializers.ModelSerializer):
	category1=Category1AbstractSerializer()
	category2=Category2AbstractSerializer()
	class Meta:
		model = Record
		exclude=[]
		
class RecordCommentsSerializer(serializers.ModelSerializer):
	profile=ProfileSerializer(required=False)
	record=RecordDetailSerializer(required=False)
	class Meta:
		model=RecordComments
		fields='__all__'

	def save(self,user123,record1):
		profile1=Profile.objects.get(user=user123)
		record=None
		record=record1
		if('comment' in self.validated_data.keys()):
			comment_field=self.validated_data['comment']
			comment=RecordComments.objects.create(
				profile=profile1,
				record=record,
				comment=comment_field
				)
			record1.no_of_comments+=1
			record1.save()
			comment.save()
			return comment
		else:
			raise serializers.ValidationError({'comment_field_is_mandatory':'Comment field is mandatory'})	

class RecordLikesSerializer(serializers.ModelSerializer):
	profile=ProfileSerializer(required=False)
	class Meta:
		model=RecordLikes
		exclude=[]

