from django.contrib import admin
from .models import Post, Response, Newsletter, Subscription

admin.site.register(Post)
admin.site.register(Response)
admin.site.register(Newsletter)
admin.site.register(Subscription)