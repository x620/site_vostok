# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import random

from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from photos.models import Tag, Photo, Like

TAGS_COUNT = 100
TAGS = ['tag_%s' % str(i + 1).zfill(3) for i in range(TAGS_COUNT)]


class Command(BaseCommand):
	help = 'Create tags for photos'

	def handle(self, *args, **options):
		count_like = count_photo = 0
		users = list(User.objects.values_list('id', flat=True))

		start = timer = time.time()
		photos = Photo.objects.prefetch_related().all()[3:]
		for photo in photos:
			random.shuffle(users)
			users_ids = users[:random.randint(0, 10)]
			for user_id in users_ids:
				like, created = Like.objects.get_or_create(user_id=user_id, photo=photo)
				if created:
					count_like += 1
					# print('Photo: %s. User: %s. %s.' % (photo, user_id, like))
			count_photo += 1

			if time.time() - timer > 60.0:
				print('Now: %s. Update %s photos. Create %s likes.' % (datetime.now(), count_photo, count_like))
				timer = time.time()

		print('Time: %s s' % (time.time() - start))

		message = 'Create likes for photos'
		self.stdout.write(self.style.SUCCESS(message))

