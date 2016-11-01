# coding=utf-8
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from web.models import *

# Create your views here.
def main(request):
    return render(request, 'main.html', {'string': "我是变量"})

def showtop1000(request):
    page = int(request.POST.get('pageNum', 1))
    limit = int(request.POST.get('numPerPage', 20))
    keyword = request.POST.get('keyword', '')
    if keyword:
        actors = Actor.objects.filter(name__contains=keyword)
    else:
        actors = Actor.objects.all()
    paginator = Paginator(actors, limit)
    paginator.currentpage = page
    try:
        actors = paginator.page(page)
    except PageNotAnInteger:
        actors = paginator.page(1)
    except EmptyPage:
        actors = paginator.page(paginator.num_pages)
    return render(request, 'top1000.html', {
        'actors': actors,
        'paginator': paginator,
        'pagestart': str((page - 1) * limit),
        'keyword': keyword
    })
