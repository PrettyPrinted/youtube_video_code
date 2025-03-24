from django.shortcuts import render, redirect

from .tasks import generate_image
from .models import Image

def index(request):
    if request.method == "POST":
        prompt = request.POST["prompt"]
        generate_image.delay(prompt)
        return redirect("index")

    context = {
        "images": Image.objects.all()
    }
    
    return render(request, "index.html", context)
