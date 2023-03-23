from django.contrib import admin

from .models import Messages, Groups

# Register your models here.
admin.site.register(Messages)
admin.site.register(Groups)