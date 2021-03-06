import datetime

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, Http404
from django.conf import settings

from teams.models import Team
from feeds.models import Post
from accounts.forms import LoginForm
from utilities.utils import create_form

def home(request, template=None):
    '''Home page'''
    # Standings
    teams = Team.objects.all()
    teams_sort_by_distance = sorted(teams, key=lambda x: x.distance, reverse=True)
    
    # Feed
    posts = Post.objects.all().order_by('-time').select_related('team')

    # Stats
    total_amount_raised = sum([team.amount_raised for team in teams])
    total_distance_from_start = sum([team.distance for team in teams])

    # timer related stuff
    started = False
    seconds_to_start = (settings.START_TIME - datetime.datetime.now()).total_seconds()
    if seconds_to_start < 0:
        seconds_to_start = 0
        started = True
    print seconds_to_start

    return render(request, template, {
            'standings': teams_sort_by_distance,
            'posts': posts,
            'total_amount_raised': total_amount_raised,
            'total_distance_from_start': int(total_distance_from_start),
            'STARTED': started,
            'seconds_to_start': seconds_to_start,
            'home_page': True
        })

def login(request, template=None):
    '''User login page'''

    login_form = create_form(LoginForm, request, request)
    if request.method == 'POST':
        login_form.save()

        return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, template, {
            'login_form': login_form,
            'login_page': True
        })

@login_required
def logout(request):
    '''User logout page'''
    logout(request)

    return render(request, template, {
            'logout_page': True
        })

@login_required
def profile(request, template):
    '''Users profile page'''

    return render(request, template, {
            'profile_page': True
        })


