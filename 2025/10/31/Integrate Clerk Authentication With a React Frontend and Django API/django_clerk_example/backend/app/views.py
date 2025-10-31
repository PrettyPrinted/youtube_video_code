from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .models import Video

class VideoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.filter(channel__owner=request.user)
        video_data = [{"id": video.id, "title": video.title, "channel": video.channel.name} for video in videos]
        return Response(video_data, status=HTTP_200_OK)