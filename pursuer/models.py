from __future__ import unicode_literals

from django.db import models


class Man(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    follow_ids = models.TextField()

    class Meta:
        db_table = 'man_man'

    def __unicode__(self):
        return self.name
