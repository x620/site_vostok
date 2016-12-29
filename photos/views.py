# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Count
from models import Photo, Tag

import logging


logger = logging.getLogger(__name__)

PHOTOS_PER_PAGE = 20
ACTIONS = 'filter_tags', 'exclude_tags'


def get_tags(exclude=False):
	return Tag.objects.filter(exclude=exclude)


class MainView(ListView):
	model = Photo
	context_object_name = 'photos'
	template_name = 'main.html'
	paginate_by = PHOTOS_PER_PAGE

	def get(self, request, *args, **kwargs):
		for tag_type in ACTIONS:
			if tag_type not in self.request.session:
				self.request.session[tag_type] = []

		# Нужно для сортировки по количеству лайков
		self.queryset = self.get_queryset().annotate(likes_count=Count('likes', distinct=True))

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
				for tag_type in ACTIONS:
					if un_tag_id in self.request.session.get(tag_type, []):
						self.request.session[tag_type] = [i for i in self.request.session.get(tag_type, []) if i != un_tag_id]
						return HttpResponseRedirect(reverse('index'))
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

		# Задаем для таблицы сохраненный вариант сортировки
		self.ordering = self.request.session.get('ordering', 'created_datetime')

		return super(MainView, self).get(request, *args, **kwargs)

	def tags_filter(self, action='filter'):
		"""Собираем выбранные теги"""
		action_type = '%s_tags' % action
		return Tag.objects.filter(id__in=self.request.session.get(action_type, []))

	def tags_remain(self):
		"""Собираем доступные для выбора теги. То есть исключаем те, которые уже были выбраны"""
		tags = get_tags()
		for action_type in ACTIONS:
			tags = tags.exclude(id__in=self.request.session.get(action_type, []))
		return tags

	def get_queryset(self):
		"""Выбираем только те фотки, которые удовлетворяют выбранным тегам (если они выбраны)"""

		queryset = super(MainView, self).get_queryset()

		filter_tags = self.request.session.get('filter_tags', [])
		if filter_tags:
			queryset = queryset.filter(tags__id__in=filter_tags)

		exclude_tags = self.request.session.get('exclude_tags', [])
		if exclude_tags:
			queryset = queryset.exclude(tags__id__in=exclude_tags)

		return queryset

	def get_context_data(self, **kwargs):
		context = super(MainView, self).get_context_data(**kwargs)
		context['main'] = True
		context['tags_filter'] = self.tags_filter()
		context['tags_exclude'] = self.tags_filter('exclude')
		context['tags_remain'] = self.tags_remain()
		return context
