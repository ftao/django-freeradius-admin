# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key
models.signals.post_save.connect(create_api_key, sender=User)

