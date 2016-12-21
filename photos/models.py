# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
	name = models.CharField('Tag name', max_length=25, unique=True)
	exclude = models.BooleanField('Exclude', default=False)


class Photo(models.Model):
	user = models.ForeignKey(User)
	url = models.CharField('Url', max_length=255, unique=True)
	created_datetime = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return '%s (%s)' % (self.pk, self.user)


class Like(models.Model):
	user = models.ForeignKey(User)
	photo = models.ForeignKey(Photo)
