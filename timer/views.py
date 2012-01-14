from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from timer.models import Meeting, Attendee, Time, Group
from timer.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect

# Homepage views
def home(request):
    if request.subdomain is not None:
        return group(request, request.subdomain)
    return render(request,'index.html',{})
    
def timer(request):
    return

def meeting(request, meeting_id):
    try:
        meeting = Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return HttpResponse("invalid meeting")
    if meeting.group.owner != request.user:
        return HttpResponse("You don't have access to this!")
    return render(request, 'meeting.html', {'meeting': meeting, 'group': meeting.group})

def redirectme(request):
    if request.user.is_authenticated():
        try:
            group = Group.objects.get(owner=request.user)
        except Group.DoesNotExist:
            return HttpResponse("group error is broken")
        return redirect('http://'+group.urltag+'.meetrx.com');
    else:
        return redirect('/login/');

def group(request, group_id):
    try:
        group = Group.objects.get(urltag=group_id,owner=request.user)
    except Group.DoesNotExist:
        return HttpResponse("Invalid Group!!")
    return render(request,'group_main.html',{'group':group, 'test':request.subdomain})
    
@csrf_protect
def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # Generate a username and create user
            new_user=User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
            #new_user.first_name=form.cleaned_data['first_name']
            #new_user.last_name=form.cleaned_data['last_name']
            new_user.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            group=Group.objects.create(name=form.cleaned_data['name'],urltag=form.cleaned_data['subdomain'], owner=new_user)
            return redirect('http://'+group.urltag+'.meetrx.com');
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
        return HttpResponse('{"error":"Invalid meeting info"}')
    try:
        group = Group.objects.get(owner=request.user)
    except Group.DoesNotExist:
        return HttpResponse('{"error":"Invalid group authentication"}')
    m=Meeting.objects.create(name=request.POST['name'], group=group)
    return HttpResponse('{ "id": "'+str(m.pk)+'" }')
    
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