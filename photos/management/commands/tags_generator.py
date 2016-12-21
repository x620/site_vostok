# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from photos.models import Tag

TAGS_COUNT = 100
TAGS = ['tag_%s' % str(i + 1).zfill(3) for i in range(TAGS_COUNT)]


class Command(BaseCommand):
	help = 'Create tags to Tag model'

	def handle(self, *args, **options):
		create_count = 0

		for tag_name in TAGS:
			new_tag, created = Tag.objects.get_or_create(name=tag_name)
			if created:
				create_count += 1

		if create_count:
			message = 'Successfully generate tags. Created %s tags' % create_count
		else:
			message = 'Such tags already exist. So tags were not added.'
		self.stdout.write(self.style.SUCCESS(message))
