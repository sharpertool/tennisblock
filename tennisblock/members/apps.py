# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

class MembersConfig(AppConfig):

    name = "members"
    verbose_name = "Members App Config"

    def ready(self):
        import members.signals
        super(MembersConfig, self).ready()
