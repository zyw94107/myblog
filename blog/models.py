from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
import markdown
from myblog import settings
from django.utils.html import strip_tags


# Create your models here.

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()

    # 创建 修改时间
    creat_time = models.DateTimeField()
    modify_time = models.DateTimeField()

    # 文章摘要
    excerpt = models.CharField(max_length=200, blank=True)

    # 类型  外键 一堆多
    category = models.ForeignKey(Category)
    # 标签  多对多
    tag = models.ManyToManyField(Tag, blank=True)

    # user
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    views = models.PositiveIntegerField(default=0)  # 只为正数

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-creat_time']
