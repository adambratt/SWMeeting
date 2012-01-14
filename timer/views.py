from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from timer.models import Meeting, Attendee, Time, Group
from timer.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Homepage views
def home(request):
    if request.subdomain is not None:
        return group(request, request.subdomain)
    return render(request,'index.html',{})
    
def timer(request):
    return

def group(request, group_id):
    try:
        group = Group.objects.get(urltag=group_id)
    except Group.DoesNotExist:
        return HttpResponse("Invalid Group!!")
    return render(request,'group_main.html',{'group':group, 'test':request.subdomain})
    
def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # Generate a username and create user
            new_user=User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
            #new_user.first_name=form.cleaned_data['first_name']
            #new_user.last_name=form.cleaned_data['last_name']
            new_user.save()
            new_user = authenticate(username=username, password=form.cleaned_data['password1'])
            login(request, new_user)
            group=Group.objects.create(name=form.cleand_data['name'],urltag=form.cleaned_data['subdomain'])
            return redirect(group.subdomain+'.meetrx.com');
    else:
        form=RegistrationForm()
    return render(request,'registration.html',{'form':form})

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