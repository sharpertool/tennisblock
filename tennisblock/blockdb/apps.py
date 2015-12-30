# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings

from .receivers import define_receivers

class BlockDBConfig(AppConfig):

    name = "blockdb"
    verbose_name = "Block Database App"

    def ready(self):
        #User = self.get_model(settings.AUTH_USER_MODEL)
        #Season = self.get_model('Season')
        define_receivers()
