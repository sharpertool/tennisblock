# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings

class BlockDBConfig(AppConfig):

    name = "blockdb"
    verbose_name = "Block Database App"

    def ready(self):
        import blockdb.signals
        super(BlockDBConfig, self).ready()
