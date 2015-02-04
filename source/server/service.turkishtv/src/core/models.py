
from django.db import models

class AppMeta(models.Model):
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)
    class Meta:
        verbose_name="App Metadata"
        verbose_name_plural="App Metadata"
    def __unicode__():
        return self.key

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.IntegerField(max_length=5)
    label = models.CharField(max_length=128)
    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categories"
    def __unicode__(self):
        return self.label

class StreamType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    #TODO - Flesh this out to describe how to handle different StreamTypes
    class Meta:
        verbose_name="Stream Type"
        verbose_name_plural="Stream Types"
    def __unicode__(self):
        return self.name

class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=96)
    category = models.ForeignKey(Category)
    stream_type = models.ForeignKey(StreamType)
    url_icon = models.URLField(null=True, blank=True)
    url_stream = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    class Meta:
        verbose_name="Channel"
        verbose_name_plural="Channels"
    def __unicode__(self):
        return self.name
