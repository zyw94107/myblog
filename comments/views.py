from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm


# Create your views here.


def post_comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':

        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form = CommentForm(request.POST)
        if form.is_valid():  # 检测form是否合法
            comment = form.save(commit=False)  # 生成Comment模型类的实例，并不保存到数据库
            comment.post = post  # 将comment 和 post 关联起来
            comment.save()
            return redirect(post)  # redirect函数接受实例 调用 post的get_absolute_url方法获取url 重定向到此url
        else:
            comment_list = post.comment_set.all()  # 因为post和comment是外键关联 反向查询全部评论
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list,
                       }
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)
