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
     url(r'^$','timer.views.home'),
     url(r'^home/$','timer.views.redirectme'),
     url(r'^payment/$','timer.views.payment'),
     url(r'^register/$','timer.views.register'),
     url(r'^logout/$', 'django.contrib.auth.views.logout'),
     url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
     url(r'^meeting/(?P<meeting_id>\w+)/$', 'timer.views.meeting'),
     url(r'^report/(?P<meeting_id>\w+)/$', 'timer.views.report'),
     url(r'^ajax/log/(?P<meeting_id>\w+)/(?P<attendee_id>\w+)/$', 'timer.views.log'),
     url(r'^ajax/create_meeting/$', 'timer.views.create_meeting'),
     url(r'^ajax/create_attendee/$', 'timer.views.create_attendee'),
     url(r'^ajax/add_attendee/(?P<meeting_id>\w+)/(?P<attendee_id>\w+)/$', 'timer.views.add_attendee'),
     url(r'^(?P<group_id>\w+)/$', 'timer.views.group'),
)
