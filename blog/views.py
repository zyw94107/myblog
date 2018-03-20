from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import  Post,Category
from comments.forms import CommentForm
import markdown
# Create your views here.

def index(request):
    post_list = Post.objects.all()
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
    form = CommentForm()
    comment_list = post.comment_set.all()
    context ={
        'post':post,
        'comment_list':comment_list,
        'form':form
    }
    return render(request,'blog/detail.html',context=context)

def archives(request,year,month):
    post_list=Post.objects.filter(creat_time__year=year,
                                  creat_time__month=month,
                                  )
    return render(request,'blog/index.html',context={'post_list':post_list})

def categories(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate)
    return render(request,'blog/index.html',context={'post_list':post_list})