from django.db import models
from datetime import datetime

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class PostalCodeInfo(models.Model):
    postal_code = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()

class Person(models.Model):
    ssn = models.CharField(blank=True,max_length=20)
    age = models.IntegerField()

class Metric(models.Model):
    date = models.DateTimeField(blank=True)
    ssn = models.ForeignKey(
        Person,
        on_delete=models.DO_NOTHING
    )
    reason = models.IntegerField()
    postal_code = models.ForeignKey(
		PostalCodeInfo,
		on_delete=models.DO_NOTHING
	)
    extras = models.CharField(blank=True,max_length=50)
