from django.db import models


class Regions(models.Model):
    region = models.CharField(max_length=20)

    class Meta:
        db_table = 'regions'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.region