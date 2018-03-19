from ..models import Post,Category
from django import template

register = template.Library()
#导入template包 并实例化Library类 并且将函数装饰register.simple_tag，这样就能在模板中使用了


@register.simple_tag
def get_recent_post(num=5):#获得最近5篇文章 最新文章标签
    return Post.objects.all().order_by('-creat_time')[:num]

@register.simple_tag
def archive():#归档模版标签
    return Post.objects.dates('creat_time','month',order='DESC')

@register.simple_tag
def get_category():#分类标签
    return Category.objects.all()