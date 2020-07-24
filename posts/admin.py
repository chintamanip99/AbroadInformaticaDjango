from django.contrib import admin
from .models import Channels,Posts,Likes,Comments
# Register your models here.

admin.site.register(Channels)
admin.site.register(Posts)
admin.site.register(Likes)
admin.site.register(Comments)