# -*- coding: utf-8 -*-
import csv
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from site_vostok.settings import BASE_DIR

LIMIT = 10
FILENAME = 'test-photo.csv'


class Command(BaseCommand):
	help = 'Create images to Photo model from test-photo.csv'

	def handle(self, *args, **options):
		csv_filename = os.path.join(BASE_DIR, FILENAME)
		if os.path.exists(csv_filename):
			with open(csv_filename, 'rb') as csv_file:
				created_count = count = 0
				data = csv.reader(csv_file, delimiter=';')
				for row in data:
					if data.line_num == 1:
						continue

					# TODO: Create image to Photo model
					print('Image url: %s. Added datetime: %s' % (row[1], row[2]))

					count += 1
					if count >= LIMIT:
						break

				self.stdout.write(self.style.SUCCESS('Successfully generate. Created %s images' % created_count))
		else:
			self.stdout.write(self.style.SUCCESS('File %s not exists' % csv_filename))

