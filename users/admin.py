from django.contrib import admin
from .models import Profile
from home.models import Blog, Comment, UserViews, BlogViews
from tinymce.widgets import TinyMCE
from django.db import models


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Private Information", {
            "fields": (
                ["user", "date_of_birth", "bio", "location", "image", "user_name"]
            ),
        })
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(Profile, ProfileAdmin)


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/Date", {
            "fields": (
                ["title", "date_posted"]
            ),
        }),
        ("Author", {
            "fields": (
                ["author"]
            )
        }),
        ("Content", {
            "fields": (
                ["content"]
            )
        })
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(Blog, BlogAdmin)


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Author of Comment", {
            "fields": (
                ["user_to_comment"]
            ),
        }),
        ("Comment to which Post", {
            "fields": (
                ["comment_to_post"]
            )
        }),
        ("Comment", {
            "fields": (
                ["comment"]
            )
        }),
        ("Date of Comment", {
            "fields": (
                ["date_commented"]
            )
        })
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(Comment, CommentAdmin)

admin.site.register(BlogViews)
admin.site.register(UserViews)
