from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class gcfnote(models.Model):
    po = models.CharField(max_length=45, unique=True)
    timestamp = models.DateTimeField()
    model = models.CharField(max_length=45)
    family = models.CharField(max_length=45)
    level = models.CharField(max_length=45)
    region = models.CharField(max_length=45)
    ctomod = models.CharField(max_length=45)
    destination = models.CharField(max_length=45)
    OSP = models.CharField(max_length=45)
    OSD = models.CharField(max_length=45)
    OSV = models.CharField(max_length=45)
    muiflag = models.BooleanField(default=False)
    cfiflag = models.BooleanField(default=False)
    siaccount = models.CharField(max_length=45, null = True, blank = True)
    mod = models.TextField()
    sdr = models.TextField()
    filepath = models.CharField(max_length=80)

    def __unicode__(self):
        return self.po

class gcfAdmin(admin.ModelAdmin):
    list_display = ('po', 'level', 'family', 'model', 'destination', 'timestamp','OSV', 'OSP', 'OSD', 'filepath')
    # list_filter = ('OSP',)

    search_fields = ('po', 'family','sdr')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

    fieldsets = [
            ('Basic information',  {
                'fields':('po', 'level', 'family', 'model', 'destination', 'region', 'ctomod', 'OSV', 'OSP', 'OSD','muiflag', 'cfiflag', 'siaccount')
            }),
            ('Advanced information',{
                'fields':('timestamp', 'mod', 'sdr', 'filepath'),
                'classes':('collapse',)
            })
                ]

admin.site.register(gcfnote, gcfAdmin)
