# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from models import Photo, Tag
from django.core.paginator import PageNotAnInteger, EmptyPage
import logging

from django.views.generic import ListView

logger = logging.getLogger(__name__)

PHOTOS_PER_PAGE = 20


def get_tags(exclude=False):
	return Tag.objects.filter(exclude=exclude)


class MainView(ListView):
	queryset = Photo.objects.all()
	context_object_name = 'photos'
	template_name = 'main.html'

	def __init__(self, **kwargs):
		super(MainView, self).__init__(**kwargs)
		self.tag_filter = []

	def get(self, request, *args, **kwargs):
		if request.GET.get('tag'):
			try:
				s = request.GET.get('tag').split(',')
				for i in s:
					try:
						self.tag_filter.append(int(i))
					except:
						pass
			except:
				pass
		return super(MainView, self).get(request, *args, **kwargs)

	def tags_filter(self):
		# Собираем выбранные теги
		tags_filter = []
		for tag_id in self.tag_filter:
			try:
				tags_filter.append(Tag.objects.get(pk=tag_id))
			except:
				pass
		return tags_filter

	def tags_remain(self):
		# Собираем доступные для выбора теги
		tags = get_tags()
		for tag_filter in self.tags_filter():
			tags = tags.exclude(id=tag_filter.id)
		return tags

	def get_queryset(self):
		# Выбираем только те фотки, которые удовлетворяют выбранным тегам (если они выбраны)
		if self.tag_filter:
			for tf in self.tag_filter:
				self.queryset = self.queryset.filter(tags__id=tf)
		return self.queryset

	def get_context_data(self, **kwargs):
		paginator = self.get_paginator(self.get_queryset(), PHOTOS_PER_PAGE)
		page = self.request.GET.get('page')

		try:
			photos_table = paginator.page(page)
		except PageNotAnInteger:
			photos_table = paginator.page(1)
		except EmptyPage:
			photos_table = paginator.page(paginator.num_pages)

		context = super(MainView, self).get_context_data(**kwargs)
		context['main'] = True
		context['photos_table'] = photos_table
		context['tags_filter'] = self.tags_filter()
		context['tags_remain'] = self.tags_remain()
		context['page'] = page
		return context
