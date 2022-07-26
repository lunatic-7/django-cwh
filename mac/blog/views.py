from django.http import HttpResponse
from django.shortcuts import render

from .models import Blogpost

# Create your views here.
def index(request):
    blogs = Blogpost.objects.all()
    params = {'blog': blogs}
    return render(request, 'blog/index.html', params)

def blogpost(request, id):
    post = Blogpost.objects.filter(post_id = id)[0]
    return render(request, 'blog/blogpost.html', {'post': post})
