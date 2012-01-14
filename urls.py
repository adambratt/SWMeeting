from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'meeting.views.home', name='home'),
    # url(r'^meeting/', include('meeting.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$','timer.home'),
     url(r'^ajax/log/(?P<meeting_id>\w+)/(?P<attendee_id>\w+)/$', 'timer.log'),
     url(r'^ajax/create_meeting/$', 'timer.create_meeting'),
     url(r'^ajax/create_attendee/$', 'timer.create_attendee'),
     url(r'^ajax/add_attendee/(?P<meeting_id>\w+)/(?P<attendee_id>\w+)/$', 'timer.add_attendee'),
)
