from django.contrib import admin

from .models import Actor, Movie, Comment

admin.site.register([Actor, Movie, Comment])
