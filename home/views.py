from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from studygroups.models import Course, CurrentSemester, Subject
from courses.forms import SearchForm
from courses.views import SearchTemplate
from django.shortcuts import redirect

def index(request):
    template = 'home.html'
    form = SearchForm() # An unbound form
     
    context = SearchTemplate.context
    
    return render(request, template, context)