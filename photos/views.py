# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from models import Photo, Tag
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.db.models import Count
import logging

from django.views.generic import ListView

logger = logging.getLogger(__name__)

PHOTOS_PER_PAGE = 20


def get_tags(exclude=False):
	return Tag.objects.filter(exclude=exclude)


class MainView(ListView):
	model = Photo
	context_object_name = 'photos'
	template_name = 'main.html'

	def __init__(self, **kwargs):
		super(MainView, self).__init__(**kwargs)

	def get(self, request, *args, **kwargs):
		actions = 'filter_tags', 'exclude_tags'
		for tag_type in actions:
			if tag_type not in self.request.session:
				self.request.session[tag_type] = []

		# Нужно для сортировки по количеству лайков
		self.queryset = self.get_queryset().annotate(likes_count=Count('likes'))

		action = request.GET.get('action_type')
		# Получаем из GET id по тегу filter или exclude
		if action:
			tag_type = '%s_tags' % action
			# Добавление id тега в сессию
			tag_id = request.GET.get('tag')
			try:
				if tag_id is not None:
					tag_id = int(tag_id)
					if tag_id not in self.request.session.get(tag_type, []):
						if action == 'exclude' and len(self.request.session.get(tag_type)) >= 3:
							# TODO: Обработка события, когда добавляется слищком много тегов-исключений
							print('Нельзя добавлять больше 3 тегов-исключений')
						else:
							self.request.session[tag_type] += [tag_id]
			except ValueError:
				logger.error('%s tags id "%s" is not integer' % (action.upper(), tag_id))

		# Удаление id тега из сессии
		un_tag_id = request.GET.get('un_tag')
		try:
			if un_tag_id is not None:
				un_tag_id = int(un_tag_id)
				for tag_type in actions:
					if un_tag_id in self.request.session.get(tag_type, []):
						self.request.session[tag_type] = [i for i in self.request.session.get(tag_type, []) if i != un_tag_id]
						# return HttpResponseRedirect(reverse('index'))
		except ValueError:
			logger.error('Tags id "%s" is not integer' % un_tag_id)

		# Сортировка
		sorting = request.GET.get('sorting')
		if sorting is not None:
			# Получаем сохраненный в сессии вариант сортировки
			ordering = self.request.session.get('ordering', '-created_datetime')

			# Задаем варианты сортировки
			v = '-created_datetime', 'created_datetime'
			if sorting == 'likes':
				v = '-likes_count', 'likes_count'

			# Выбираем вариант сортировки
			self.request.session['ordering'] = v[1] if ordering == v[0] else v[0]

		return super(MainView, self).get(request, *args, **kwargs)

	def tags_filter(self, action='filter'):
		# Собираем выбранные теги
		tags_filter = []
		action_type = '%s_tags' % action
		for tag_id in self.request.session.get(action_type, []):
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
		for tag_filter in self.tags_filter('exclude'):
			tags = tags.exclude(id=tag_filter.id)
		return tags

	def get_queryset(self):
		# Выбираем только те фотки, которые удовлетворяют выбранным тегам (если они выбраны)
		queryset = super(MainView, self).get_queryset()
		filter_tags = self.request.session.get('filter_tags', [])
		if filter_tags:
			# Создаем пустой queryset
			qs = Tag.objects.none()
			for tf in filter_tags:
				try:
					# Выбираем теги соответствующие очередному тегу и добавляем в qs
					qs |= queryset.filter(tags__id=tf)
				except:
					pass
			queryset = qs
		exclude_tags = self.request.session.get('exclude_tags', [])
		if exclude_tags:
			for te in exclude_tags:
				# Выбираем теги соответствующие очередному тегу и исключаем из queryset
				queryset = queryset.exclude(tags__id=te)
		return queryset

	def get_photos_table(self):
		# Пейджинг
		paginator = self.get_paginator(self.get_queryset(), PHOTOS_PER_PAGE)
		page = self.kwargs.get('page', 1)
		try:
			photos_table = paginator.page(page)
		except PageNotAnInteger:
			photos_table = paginator.page(1)
		except EmptyPage:
			photos_table = paginator.page(paginator.num_pages)
		return photos_table

	def get_context_data(self, **kwargs):
		# Задаем для таблицы сохраненный вариант сортировки
		self.ordering = self.request.session.get('ordering', '-created_datetime')

		# Пейджинг
		paginator = self.get_paginator(self.get_queryset(), PHOTOS_PER_PAGE)
		page = self.kwargs.get('page', 1)
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
		context['tags_exclude'] = self.tags_filter('exclude')
		context['tags_remain'] = self.tags_remain()
		return context
