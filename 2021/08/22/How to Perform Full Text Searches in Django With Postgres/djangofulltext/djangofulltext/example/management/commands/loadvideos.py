import requests

from django.core.management.base import BaseCommand, CommandError

from example.models import Video

class Command(BaseCommand):
    help = 'Loads data from the 50 most recent YouTube videos on the given channel.'

    def handle(self, *args, **options):
        key = 'YOUR-YOUTUBE-API-KEY'
        channel_id = 'UC-QDfvrRIDB6F0bIO4I4HkQ'

        url = f'https://www.googleapis.com/youtube/v3/channels?id={channel_id}&key={key}&part=contentDetails'
        r = requests.get(url)

        channel = r.json()['items'][0]
        playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

        url = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&key={key}&part=contentDetails,snippet&maxResults=50'
        r = requests.get(url)

        data = r.json()
        results = data['items']
    
        for item in results:
            youtube_id = item['contentDetails']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            video = Video(youtube_id=youtube_id, title=title, description=description)
            video.save()