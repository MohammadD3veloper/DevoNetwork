from django.contrib import admin

from .models import User, UserContacts, UserImages

# Register your models here.
admin.site.register(User)
admin.site.register(UserContacts)
admin.site.register(UserImages)
