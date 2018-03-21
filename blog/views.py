from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from .models import  Post,Category,Tag
from comments.forms import CommentForm
import markdown
# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = '2'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated=context.get('is_paginated')

        pagination_data=self.pagination_data(paginator,page,is_paginated)
        context.update(pagination_data)
        return context
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}
        left=[]
        right=[]
        left_has_more=False
        right_has_more=False
        first = False #是否显示第一
        last = False #是否显示最后
        page_number=page.number#page为上面传入的page_obj实例 用于获取当前页数
        total_pages = paginator.num_pages #获得总页数
        page_range = paginator.page_range #获得页码列表

        if page_number == 1:
            right = page_range[page_number:page_number + 2 ]#右边是 2 3
            if right[-1] < total_pages - 1 :
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number -3)>0 else 0:page_number-1]
            if left[0]>2:
                left_has_more = True
            if left[0]>1:
                first =True
        else:
            left=page_range[(page_number -3 )if (page_number-3)>0 else 0:page_number-1]
            right=page_range[page_number:page_number+2]

            #是否要显示后省略号
            if right[-1] < total_pages-1:
                right_has_more = True
            if right[-1] < total_pages :
                last =True
            #是否显示前省略号
            if left[0]>2:
                left_has_more =True
            if left[0]>1:
                first = True

        data={
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self,request,*args,**kwargs):
        response = super(PostDetailView,self).get(request,*args,**kwargs)#需先调用父类的get方法，才能得到object
        self.object.increase_views()
        return response  #必须返回HttpResponse对象
    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView,self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                ])
        return post
    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'comment_list': comment_list,
            'form': form
        })
        return context

class ArchivesView(IndexView):
    def get_queryset(self):

        return super(ArchivesView,self).get_queryset().filter(creat_time__year=self.kwargs.get('year'),
                                                          creat_time__month=self.kwargs.get('month'),
                                                          )

class CategoryView(IndexView):
    def get_queryset(self):#该父类方法主动获取所有列表数据，复写添加获取条件
        cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

class TagsView(IndexView):
    def get_queryset(self):
        tag =get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagsView,self).get_queryset().filter(tag=tag)

