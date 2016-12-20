# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class MainView(TemplateView):
	template_name = 'main.html'

	def get_context_data(self, **kwargs):
		context = super(MainView, self).get_context_data(**kwargs)
		context['main'] = True
		return context
