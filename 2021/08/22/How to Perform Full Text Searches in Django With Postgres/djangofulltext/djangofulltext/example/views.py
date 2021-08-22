from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline

from .models import Video

def index(request):
    q = request.GET.get('q')

    if q:
        vector = SearchVector('title', 'description')
        query = SearchQuery(q)
        search_headline = SearchHeadline('description', query)

        #videos = Video.objects.filter(title__search=q)
        #videos = Video.objects.annotate(search=vector).filter(search=query)
        #videos = Video.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')
        videos = Video.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline).filter(rank__gte=0.001).order_by('-rank')
    else:
        videos = None

    
    context = {'videos' : videos}
    return render(request, 'example/index.html', context)
