# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Photo, Tag, Like


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'created_datetime')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'exclude')
	search_fields = ('name',)
	list_filter = ('exclude',)
	list_editable = ('exclude',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
	list_display = ('user', 'photo')
