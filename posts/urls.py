from django.urls import path,include
from .views import Channel,Post,Like,Comment,StandardResultsSetPagination
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from BhagwaPataka.urls import IsConfirmedEmail
from django.conf.urls.static import static
from django.conf import settings

# @api_view(['GET'])
# @permission_classes([(IsConfirmedEmail)])
# def protected_serve(request, path, document_root=None, show_indexes=False):
#     if(request.user.is_authenticated):
#         return serve(request, path, document_root, show_indexes)
#     else:
#         return Response({'authentication':'Authentication Credentials not provided'})

app_name="posts"
urlpatterns = [
    path('channel/<int:type>',Channel.as_view(),name='channel'),
    path('post/<int:id>',Post.as_view(),name='post'),
    path('like/<int:id>',Like.as_view(),name='like'),
    path('comment/<int:id>',Comment.as_view(),name='comment'),
]

