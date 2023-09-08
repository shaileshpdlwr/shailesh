from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from taggit.managers import TaggableManager


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=100,unique_for_date='publish')
    slug=models.SlugField(max_length=200)
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=CustomManager()
    tags=TaggableManager()   #For search engine Optimization # For easy navigation to the end user

    class Meta:
        ordering=('-publish',)
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.slug])


class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    email=models.EmailField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    body=models.TextField()
    active=models.BooleanField(default=True)
    class Meta:
        ordering=('-created',)
    def __str__(self):
        return 'commented By {} on {}'.format(self.name,self.post)

