from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from timer.models import Meeting, Attendee, Time, Group

# Homepage views
def home(request):
    return render(request,'index.html',{})
    
def timer(request):
    return

def group(request, group_id):
    try:
        group = Group.objects.get(urltag=group_id)
    except Group.DoesNotExist:
        return HttpResponse("Invalid Group!!")
    return render(request,'group_main.html',{'group':group})

# AJAX
def log(request, meeting_id, attendee_id):
    if request.method != 'POST' or 'time_start' not in request.POST or 'time_end' not in request.POST:
        return HttpResponse('Invalid post info')
    try:
        meeting = Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return HttpResponse("{'error':'Invalid meeting'}")
    try:
        attendee = Attendee.objects.get(pk=attendee_id)
    except Attendee.DoesNotExist:
        return HttpResponse("{'error':'Invalid attendee'}")
    t=Time.objects.create(meeting=meeting, attendee=attendee, time_start=request.POST['time_start'],time_end=request.POST['time_end'])
    return HttpResponse('Time Posted')

def create_meeting(request):
    if request.method != 'POST' or 'name' not in request.POST:
        return HttpResponse('Invalid post info')
    m=Meeting.objects.create(name=request.POST['name'])
    return HttpResponse('Meeting Created')
    
def create_attendee(request):
    if request.method != 'POST' or 'name' not in request.POST:
        return HttpResponse('Invalid post info')
    m=Attendee.objects.create(name=request.POST['name'])
    return HttpResponse('Attendee Created')

def add_attendee(request, meeting_id, attendee_id):
    try:
        meeting = Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return HttpResponse("{'error':'Invalid meeting'}")
    try:
        attendee = Attendee.objects.get(pk=attendee_id)
    except Attendee.DoesNotExist:
        return HttpResponse("{'error':'Invalid attendee'}")
    meeting.people.add(attendee)
    return HttpResponse('Attendee added')
    
def display(request, template, dict={}):
    try:
        group = Group.objects.get(owner=request.user)
    except Group.DoesNotExist:
        return HttpResponse("Invalid group!")
    dict['group']=group
    return render(request, template, dict)