# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import random

from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from photos.models import Photo

TAGS_COUNT = 100
TAGS = ['tag_%s' % str(i + 1).zfill(3) for i in range(TAGS_COUNT)]


class Command(BaseCommand):
	help = 'Create tags for photos'

	def handle(self, *args, **options):
		count_like = count_photo = 0
		users = list(User.objects.values_list('id', flat=True))

		start = timer = time.time()
		photos = Photo.objects.prefetch_related().all()
		for photo in photos:
			random.shuffle(users)
			users_ids = users[:random.randint(0, 10)]
			photo.likes.set(list(User.objects.filter(id__in=users_ids)))
			count_photo += 1

			if time.time() - timer > 60.0:
				print('Now: %s. Update %s photos. Create %s likes.' % (datetime.now(), count_photo, count_like))
				timer = time.time()

		print('Time: %s s' % (time.time() - start))

		message = 'Create likes for photos'
		self.stdout.write(self.style.SUCCESS(message))

