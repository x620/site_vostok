# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from models import Photo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import logging

from django.views.generic import TemplateView

logger = logging.getLogger(__name__)

PHOTOS_PER_PAGE = 20


class MainView(TemplateView):
	template_name = 'main.html'

	def get_context_data(self, **kwargs):
		photos_list = Photo.objects.all()[:100]
		paginator = Paginator(photos_list, PHOTOS_PER_PAGE)
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
