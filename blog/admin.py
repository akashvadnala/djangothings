from django.contrib import admin
from .models import *


class ContactAdmin(admin.ModelAdmin):
    list_display = ["email","msg","ans"]

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["email","msg"]


admin.site.register(Post)
admin.site.register(register_table)
admin.site.register(contact,ContactAdmin)
admin.site.register(feedback,FeedbackAdmin)
admin.site.register(Seainp)
admin.site.register(Search)