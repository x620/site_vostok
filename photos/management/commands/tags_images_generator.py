# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import random

from datetime import datetime
from django.core.management.base import BaseCommand
from photos.models import Tag, Photo


class Command(BaseCommand):
	help = 'Create tags for photos'

	def handle(self, *args, **options):
		tags = list(Tag.objects.values_list('id', flat=True))

		count = 0
		start = timer = time.time()
		photos = Photo.objects.prefetch_related().all()
		for photo in photos:
			if photo.tags.count() == 0:
				random.shuffle(tags)
				tags_ids = tags[:random.randint(1, 6)]
				tags_for_photo = Tag.objects.in_bulk(tags_ids).values()
				photo.tags.set(tags_for_photo)
				count += 1

			if time.time() - timer > 60.0:
				print('Now: %s. Update %s rows' % (datetime.now(), count))
				timer = time.time()

		print('Time: %s s' % (time.time() - start))
		message = 'Create tags for photos'
		self.stdout.write(self.style.SUCCESS(message))
