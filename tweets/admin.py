from __future__ import absolute_import

from django.contrib import admin

from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('modified', 'tweeted', 'text')
    fields = ('text', 'tweeted')
    search_fields = ('text',)
    ordering = ('created',)
