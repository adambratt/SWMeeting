from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Meeting(models.Model):
    name=models.CharField(max_length=128)
    group=models.ForeignKey('Group')
    people=models.ManyToManyField('Attendee', related_name='attendee_list')
    create_ts=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    
class Attendee(models.Model):
    name=models.CharField(max_length=128)
    create_ts=models.DateTimeField(auto_now_add=True)
    group=models.ForeignKey('Group')
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

class Group(models.Model):
    name=models.CharField(max_length=128)
    urltag=models.CharField(max_length=30)
    owner=models.ForeignKey('User')
    def __unicode__(self):
        return self.urltag