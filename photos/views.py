# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from models import Photo
from django.core.paginator import PageNotAnInteger, EmptyPage
import logging

from django.views.generic import ListView

logger = logging.getLogger(__name__)

PHOTOS_PER_PAGE = 20


class MainView(ListView):
	queryset = Photo.objects.all()[:100]
	context_object_name = 'photos'
	template_name = 'main.html'

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

		return context
