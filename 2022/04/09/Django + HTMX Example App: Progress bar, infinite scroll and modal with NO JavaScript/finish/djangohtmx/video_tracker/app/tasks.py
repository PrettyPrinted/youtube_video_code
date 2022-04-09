import requests
from datetime import datetime

from django.conf import settings

from celery import shared_task 
from celery_progress.backend import ProgressRecorder

from .models import Channel, Video 

@shared_task(bind=True)
def get_video_stats(self):
    progress_recorder = ProgressRecorder(self)

    Video.objects.all().delete()

    channels = Channel.objects.all()
    channel_ids = ','.join([channel.playlist_id for channel in channels])

    url = f'https://www.googleapis.com/youtube/v3/playlists?id={channel_ids}&part=contentDetails&key={settings.YOUTUBE_API_KEY}'
    res = requests.get(url)

    total_requests = 0

    for item in res.json()['items']:
        total_requests += int(item['contentDetails']['itemCount']) // 50 + 1

    print(total_requests)

    i = 0
    for channel in channels:
        playlist_api_url = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={channel.playlist_id}&part=snippet&maxResults=50&key={settings.YOUTUBE_API_KEY}'

        while True:
            playlist_res = requests.get(playlist_api_url)
            results = playlist_res.json()

            videos_ids = []

            for item in results['items']:
                videos_ids.append(item['snippet']['resourceId']['videoId'])

            video_ids_string = ','.join(videos_ids)

            video_api_url = f'https://www.googleapis.com/youtube/v3/videos?id={video_ids_string}&part=snippet,statistics&key={settings.YOUTUBE_API_KEY}'
            video_res = requests.get(video_api_url)


            for item in video_res.json()['items']:
                date_published = datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                video = Video(
                    title=item['snippet']['title'],
                    views=item['statistics']['viewCount'],
                    likes=item['statistics']['likeCount'],
                    youtube_id=item['id'],
                    date_published=date_published,
                    channel=channel
                )

                video.save()

            i += 1
            progress_recorder.set_progress(i, total_requests, f'On iteration {i}')

            if 'nextPageToken' in results:
                nextPageToken = results['nextPageToken']
                playlist_api_url = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={channel.playlist_id}&part=snippet&maxResults=50&key={settings.YOUTUBE_API_KEY}&pageToken={nextPageToken}'
            else:
                break