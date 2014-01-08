from django.db import models
import django.contrib.sites.models


class BackstageSite(models.Model):
    django_site = models.ForeignKey(django.contrib.sites.models.Site)
    gunicorn_port = models.IntegerField(default=0)
    uwsgi_port = models.IntegerField(default=0)
    hostnames = models.TextField(default='')
    active = models.BooleanField(default=True)

    class Meta():
        db_table = 'backstage_project'