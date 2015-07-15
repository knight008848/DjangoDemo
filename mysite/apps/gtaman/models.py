from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class gcfnote(models.Model):
    po = models.CharField(max_length=45, unique=True)
    timestamp =  models.DateTimeField()
    model = models.CharField(max_length=45)
    family = models.CharField(max_length=45)
    level = models.CharField(max_length=45)
    region = models.CharField(max_length=45)
    ctomod = models.CharField(max_length=45)
    destination = models.CharField(max_length=45)
    OSP = models.CharField(max_length=45)
    OSD = models.CharField(max_length=45)
    muiflag = models.BooleanField(default=False)
    cfiflag = models.BooleanField(default=False)
    siaccount = models.CharField(max_length=45, null = True, blank = True)
    mod = models.TextField()
    sdr = models.TextField()
    filepath =  models.CharField(max_length=80)

    def __unicode__(self):
        return self.po

class platformAdmin(admin.ModelAdmin):
    list_display = ('po', 'level', 'family', 'timestamp', 'sdr')
    search_fields = ('po',)
    ordering = ('po',)
    # fields = ('name', 'model', 'lob', 'product', 'phnum')

admin.site.register(gcfnote, platformAdmin)
