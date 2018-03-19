from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import  Post,Category
import markdown
# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-creat_time')
    return render(request,'blog/index.html',
                    context={'post_list':post_list})

def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.body=markdown.markdown(post.body,
                                extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                ])
    return render(request,'blog/detail.html',context={'post':post})

def archives(request,year,month):
    post_list=Post.objects.filter(creat_time__year=year,
                                  creat_time__month=month,
                                  ).order_by('-creat_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def categories(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate).order_by('-creat_time')
    return render(request,'blog/index.html',context={'post_list':post_list})