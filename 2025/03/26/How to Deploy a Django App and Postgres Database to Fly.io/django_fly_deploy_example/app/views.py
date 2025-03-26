from django.shortcuts import render, redirect
from urllib.parse import urlparse, parse_qs

from .models import Video

def index(request):
    if request.method == "POST":
        video_url = request.POST.get('video-url')
        Video.objects.save_video(video_url)

        return redirect('index')

    context = {
        'videos': Video.objects.all()
    }
    return render(request, 'index.html', context)