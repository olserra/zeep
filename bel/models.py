from django.db import models
from django.contrib.gis.db import models as gismodels


class House(models.Model):
    id = models.AutoField(primary_key=True)
    fuid = models.IntegerField()
    vraagprijs = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    rdx = models.CharField(max_length=255, blank=True, null=True)
    rdy = models.CharField(max_length=255, blank=True, null=True)
    geom = gismodels.PointField()
    objects = gismodels.GeoManager()

    class Meta:
        managed = True
        db_table = 'house'
