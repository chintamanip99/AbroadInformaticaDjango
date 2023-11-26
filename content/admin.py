from django.contrib import admin
from .models import (
	Category1,
	Category2,
	Record,
	RecordLikes,
	RecordComments
	)

admin.site.register(Category1)
admin.site.register(Category2)
admin.site.register(Record)
admin.site.register(RecordLikes)
admin.site.register(RecordComments)