from django.db import models

# Create your models here.
class Meeting(models.Model):
    name=models.CharField(max_length=128)
    create_ts=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name