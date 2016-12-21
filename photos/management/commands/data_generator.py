# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tags_generator import Command as GenerateTagCommand
from users_generator import Command as GenerateUserCommand
from images_generator import Command as GenerateImagesCommand


class Command(BaseCommand):
	help = '''
	Создание записей должно производиться в таком порядке
	1. Создание тегов.
	2. Создание пользователей.
	3. Создание фоток. Присваивание связей с пользователями.
	'''

	def handle(self, *args, **options):
		GenerateTagCommand().handle()
		print('')
		GenerateUserCommand().handle()
		print('')
		GenerateImagesCommand().handle()

		# TODO: 4. Присваивание фоткам тегов.
		# TODO: 5. Создание лаков для фоток.
