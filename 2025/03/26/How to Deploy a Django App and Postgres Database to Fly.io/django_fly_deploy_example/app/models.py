import requests

from django.conf import settings
from django.db import models
from urllib.parse import urlparse, parse_qs

class VideoManager(models.Manager):
    def save_video(self, video_url):
        video_id = parse_qs(urlparse(video_url).query).get('v')[0]
        
        url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={settings.YOUTUBE_API_KEY}&part=snippet,statistics'
        response = requests.get(url)
        data = response.json()

        title = data['items'][0]['snippet']['title']
        view_count = data['items'][0]['statistics']['viewCount']

        if 'maxres' in data['items'][0]['snippet']['thumbnails']:
            thumbnail_url = data['items'][0]['snippet']['thumbnails']['maxres']['url']
        else:
            thumbnail_url = data['items'][0]['snippet']['thumbnails']['high']['url']
        

        video, _ = self.get_or_create(
            yt_video_id=video_id,
            defaults={"title": title, "view_count": view_count, "thumbnail_url": thumbnail_url}
        )

        return video


class Video(models.Model):
    yt_video_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    view_count = models.IntegerField()

    objects = VideoManager()
    
    def __str__(self):
        return self.title
