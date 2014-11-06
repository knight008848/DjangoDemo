from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class platform(models.Model):
    name = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    lob = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    pebit = models.CharField(max_length=45)
    product = models.CharField(max_length=80)
    phnum = models.CharField(max_length=45, null=True)

    def __unicode__(self):
        return self.name

class platformAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'lob', 'product', 'phnum')
    search_fields = ('lob',)
    ordering = ('name',)

admin.site.register(platform, platformAdmin)