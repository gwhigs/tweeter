from __future__ import absolute_import

from django.contrib import admin

from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('created', 'tweeted', 'text')
    fields = ('text',)
    search_fields = ('text',)
    ordering = ('created',)
