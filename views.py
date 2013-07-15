# Create your views here.
import datetime
import json

from django.db.models import Q

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from linklist.models import LinkPost, Keyword
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

def index(request):
    context = dict()
    context['linkposts'] = LinkPost.objects.all()
   
    if request.user.is_authenticated():
        return render(request, 'linklist/main.html', context)

    else:
        return render(request, 'linklist/index.html', context)

def addUrl(request):
    return render(request, 'linklist/addurl.html')

def addUrlScript(request):
    result_data = dict()
    result_data['success'] = 'false'
    error = ''
    if request.method == 'POST':
        title = request.POST.get('title', '')
        url = request.POST.get('url', '')
        note = request.POST.get('note', '')

        if not title or not url:
            error = 'Error: Link post must include title and url'

        if not error:
            linkpost = LinkPost(title=title, 
                                url=url, 
                                note=note, 
                                user=request.user, 
                                dateCreated=datetime.datetime.now())
            linkpost.save()
            result_data['success'] = 'true'

    result_data['error'] = error    
    return HttpResponse(json.dumps(result_data), content_type='application/json')

def deleteUrlScript(request):
    result_data = dict()
    result_data['success'] = 'false'
    error = ''
    if request.method == 'POST':
        linkpost_id = request.POST.get('linkpost_id', '')

        if not linkpost_id:
            error = 'Error: no linkpost id'


        if not error:
            l = LinkPost.objects.get(pk=int(linkpost_id))
            l.delete()

            result_data['success'] = 'true'

    result_data['error'] = error    
    return HttpResponse(json.dumps(result_data), content_type='application/json')

def user_login(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #todo: fix login view here
            return HttpResponseRedirect('index')
        else:
            #todo: fix login view here
            return HttpResponse('error login')

def signup(request):
    context = dict()
    return render(request, 'linklist/signup.html', context)

def adduser(request):
    context = dict()
    if request.method == "POST":
        username = request.POST.get('username', 'username')
        password = request.POST.get('password', 'password')
        email = request.POST.get('email', 'blank')
        user = User.objects.create_user(username=username, 
                                        password=password,
                                        email=email)
    try:
        user.full_clean()
    except ValidationError, e:
        return HttpResponse("Something went horribly wrong :( " + str(e))
    user.save()
    user = authenticate(username=username, password=password)
    login(request, user)
    return HttpResponseRedirect("index")

def users(request):
    context = dict()
    context['users'] = User.objects.all()
    return render(request, 'linklist/users.html', context)

def isExistingUser(request):
    result_false = 'false' # username is not taken
    result_true = 'true'

    context = dict()
    user = request.POST.get('username', 'john')
    matches = User.objects.all().filter(username__exact=user)

    result = result_false
    if (len(matches) > 0):
        result = result_true

    response_data = {}
    response_data['name'] = user
    response_data['result'] = result

    return  HttpResponse(json.dumps(response_data), content_type='application/json')

def linkList(request):
    errors = []
    user = ''
    if request.user.is_authenticated():
        user = request.user
    else:
        error.append('User is not logged in')

    query = request.POST.get('query', '')

    linkposts = LinkPost.objects.all().filter(
        Q(note__icontains=query) | 
        Q(title__icontains=query),
        user=request.user)
               
    if errors:
        response = dict()
        response['error'] = error
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        context = dict()
        context['linkposts'] = linkposts
        context['query'] = query
        return render(request, 'linklist/linklist.html', context)

