from django.urls import path,include
# from .views import m
from .views import show_full_content,show_details_of_content,RecordLike,RecordComment,twilio,Content,get_server_ip_address
from django.conf import settings
from django.conf.urls.static import static

app_name="content"
urlpatterns = [
     # path('content/', m,name='m'),
     path('full_content/<int:hierarchy_level>/<int:category_id>',show_full_content,name='show_full_content'),
     path('detailed_content/<int:type>/<int:id>',show_details_of_content,name='show_details_of_content'),
     path('like/<int:id>',RecordLike.as_view(),name='rlike'),
     path('comment/<int:id>',RecordComment.as_view(),name='rcomment'),
     path('twilio/',twilio,name='twilio'),
     path('content/',Content.as_view(),name='content'),
     path('get_server_ip_address/',get_server_ip_address,name='get_server_ip_address'),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT+"/Content")
