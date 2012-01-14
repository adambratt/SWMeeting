from django.db import models

# Create your models here.
class Meeting(models.Model):
    name=models.CharField(max_length=128)
    people=models.ManyToManyField('Attendee', related_name='attendee_list')
    create_ts=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    
class Attendee(models.Model):
    name=models.CharField(max_length=128)
    create_ts=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    
class Time(models.Model):
    attendee=models.ForeignKey('Attendee')
    meeting=models.ForeignKey('Meeting')
    time_start=models.IntegerField()
    time_end=models.IntegerField()
    create_ts=models.DateTimeField(auto_now_add=True)
    
class Milestone(models.Model):
    name=models.CharField(max_length=128)
    meeting=models.ForeignKey('Meeting')
    time=models.IntegerField()
    create_ts=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name