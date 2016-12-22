# -*- coding: utf-8 -*-
import csv
import os
from datetime import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand
from site_vostok.settings import BASE_DIR
from photos.models import Photo

LIMIT = 2000
FILENAME = 'test-photo.csv'


class Command(BaseCommand):
	help = 'Create images to Photo model from test-photo.csv'

	def handle(self, *args, **options):
		csv_filename = os.path.join(BASE_DIR, 'static', 'files', 'csv', FILENAME)
		if os.path.exists(csv_filename):
			with open(csv_filename, 'rb') as csv_file:
				create_count = count = 0
				data = csv.reader(csv_file, delimiter=';')
				for row in data:
					if data.line_num == 1:
						continue

					try:
						user_id = int(row[0])
					except:
						raise TypeError("Can't convert User ID value (%s) to integer")

					created_datetime = timezone.make_aware(
						datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
						timezone.get_current_timezone()
					)
					try:
						new_photo, created = Photo.objects.get_or_create(
							user_id=user_id,
							url=row[1],
							created_datetime=created_datetime
						)
						if created:
							create_count += 1
							# print('Image url: %s. Added datetime: %s' % (row[1], created_datetime))
					except:
						continue

					count += 1
					if count >= LIMIT:
						break

				if create_count:
					message = 'Successfully generate photos. Created %s photos' % create_count
				else:
					message = 'Such photos already exist. So photos were not added.'
				self.stdout.write(self.style.SUCCESS(message))
		else:
			self.stdout.write(self.style.SUCCESS('File %s not exists' % csv_filename))

