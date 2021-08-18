from django.contrib import admin
from rare_api.models import Category, Comment, PostReaction, Post, RareUser, Reaction, Tag
# Register your models here.

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostReaction)
admin.site.register(Post)
admin.site.register(RareUser)
admin.site.register(Reaction)
admin.site.register(Tag)