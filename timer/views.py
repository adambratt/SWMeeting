from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from timer.models import Meeting, Attendee, Time, Group, Speaker, Subscription
from timer.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import stripe

# Homepage views
def home(request):
    if request.subdomain is not None:
        return group(request, request.subdomain)
    return render(request,'index.html',{})
    
def timer(request):
    return

@login_required
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

@login_required
def group(request, group_id):
    try:
        group = Group.objects.get(urltag=group_id,owner=request.user)
    except Group.DoesNotExist:
        return HttpResponse("Invalid Group!!")
    return render(request,'group_main.html',{'group':group, 'test':request.subdomain})
    
@login_required
def payment(request):
    if request.method=='POST':
        token = request.POST['stripeToken']
        stripe.api_key = "bpwTsZOTdx7UjmAjToKeXOQz9gvBGYll"
        customer = stripe.Customer.create(card=token, plan="monthly", email=request.user.email)
        sub = Subscription.objects.create(user=request.user, stripe=customer.id)
        return redirect('/');
    return render(request,'payment.html',{})
    
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
            log_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, log_user)
            group=Group.objects.create(name=form.cleaned_data['name'],urltag=form.cleaned_data['username'], owner=new_user)
            m=Attendee.objects.create(name=form.cleaned_data['username'],email=form.cleaned_data['email'],group=group)
            return redirect('http://'+group.urltag+'.meetrx.com');
    else:
        form=RegistrationForm()
    return render(request,'registration.html',{'form':form})

# AJAX
@login_required
def log(request, meeting_id, attendee_id):
    if request.method != 'POST' or 'time_start' not in request.POST or 'time_end' not in request.POST:
        return HttpResponse('Invalid post info')
    try:
        meeting = Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return HttpResponse('{"error":"Invalid meeting info"}')
    try:
        attendee = Attendee.objects.get(pk=attendee_id)
    except Attendee.DoesNotExist:
        return HttpResponse('{"error":"Invalid attendee info"}')
    try:
        speaker = Speaker.objects.get(attendee=attendee, meeting=meeting)
    except Speaker.DoesNotExist:
        return HttpResponse('{"error":"Invalid speaker info"}')
    speaker.overalltime = (int(request.POST['time_end'])-int(request.POST['time_start'])) + speaker.overalltime
    speaker.save()
    t=Time.objects.create(meeting=meeting, attendee=attendee, time_start=request.POST['time_start'],time_end=request.POST['time_end'])
    meeting.totaltime=request.POST['time_end']
    meeting.save()
    return HttpResponse('Time Posted')

@login_required
def create_meeting(request):
    if request.method != 'POST' or 'name' not in request.POST:
        return HttpResponse('{"error":"Invalid meeting info"}')
    try:
        group = Group.objects.get(owner=request.user)
    except Group.DoesNotExist:
        return HttpResponse('{"error":"Invalid group authentication"}')
    m=Meeting.objects.create(name=request.POST['name'], group=group)
    return HttpResponse('{ "id": "'+str(m.pk)+'" }')

@login_required    
def create_attendee(request):
    if request.method != 'POST' or 'name' not in request.POST:
        return HttpResponse('{"error":"Invalid attendee info"}')
    try:
        group = Group.objects.get(owner=request.user)
    except Group.DoesNotExist:
        return HttpResponse('{"error":"Invalid group authentication"}')
    m=Attendee.objects.create(name=request.POST['name'],email=request.POST['email'], group=group)
    return HttpResponse('{"id": "'+str(m.pk)+'" }')

@login_required
def add_attendee(request, meeting_id, attendee_id):
    try:
        meeting = Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return HttpResponse('{"error":"Invalid meeting"}')
    try:
        attendee = Attendee.objects.get(pk=attendee_id)
    except Attendee.DoesNotExist:
        return HttpResponse('{"error":"Invalid attendee"}')
    try:
        speaker = Speaker.objects.get(attendee=attendee, meeting=meeting)
    except Speaker.DoesNotExist:
        speaker = Speaker.objects.create(attendee=attendee, meeting=meeting)
    return HttpResponse('{"id":"'+str(speaker.pk)+'"}')
    
def display(request, template, dict={}):
    try:
        group = Group.objects.get(owner=request.user)
    except Group.DoesNotExist:
        return HttpResponse("Invalid group!")
    dict['group']=group
    return render(request, template, dict)