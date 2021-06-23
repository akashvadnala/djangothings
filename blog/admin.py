from django.contrib import admin
from .models import *


class ContactAdmin(admin.ModelAdmin):
    list_display = ["email","msg","ans"]

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["email","msg"]

class MessageModelAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'



admin.site.register(Post)
admin.site.register(register_table)
admin.site.register(contact,ContactAdmin)
admin.site.register(feedback,FeedbackAdmin)
admin.site.register(Seainp)
admin.site.register(Search)
admin.site.register(MessageModel, MessageModelAdmin)