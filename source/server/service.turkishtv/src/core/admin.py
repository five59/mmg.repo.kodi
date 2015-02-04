from django.contrib import admin
from core.models import *

#class ChannelAdmin(admin.ModelAdmin):

admin.site.register(AppMeta)
admin.site.register(Category)
admin.site.register(StreamType)
admin.site.register(Channel)
