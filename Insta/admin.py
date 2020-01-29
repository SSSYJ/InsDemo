from django.contrib import admin
from Insta.models import Post,InsUser,Like,UserConnection, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(InsUser)
admin.site.register(Like)
admin.site.register(UserConnection)
admin.site.register(Comment)