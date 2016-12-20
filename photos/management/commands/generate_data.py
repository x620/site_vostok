# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from generate_users import Command as GenerateUserCommand
from generate_images import Command as GenerateImagesCommand


class Command(BaseCommand):
	help = 'Create users to User model from test-photo.csv'

	def handle(self, *args, **options):
		GenerateUserCommand().handle()
		print('')
		GenerateImagesCommand().handle()
