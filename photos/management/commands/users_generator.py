# -*- coding: utf-8 -*-
import csv
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from site_vostok.settings import BASE_DIR

LIMIT = 10
FILENAME = 'test-photo.csv'


class Command(BaseCommand):
	help = 'Создание записей для модели User из файла test-photo.csv'

	def handle(self, *args, **options):
		csv_filename = os.path.join(BASE_DIR, FILENAME)
		if os.path.exists(csv_filename):
			with open(csv_filename, 'rb') as csv_file:
				create_count = count = 0
				data = csv.reader(csv_file, delimiter=';')
				for row in data:
					try:
						user_id = int(row[0])
					except:
						continue

					# print(user_id)

					new_user, created = User.objects.get_or_create(id=user_id, username='u%s' % user_id)
					if created:
						create_count += 1
						print('New user: %s' % user_id)

					# count += 1
					# if count >= LIMIT:
					# 	break

				if create_count:
					message = 'Successfully generate users. Created %s users' % create_count
				else:
					message = 'Such users already exist. So users were not added.'
				self.stdout.write(self.style.SUCCESS(message))
		else:
			self.stdout.write(self.style.SUCCESS('File %s not exists' % csv_filename))
