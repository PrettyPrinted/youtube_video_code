from django.shortcuts import render
from django.views.generic import ListView

from .models import Member

class MemberList(ListView):
    model = Member
