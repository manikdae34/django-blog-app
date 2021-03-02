from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


class User(AbstractUser):
    profile_img = models.ImageField(upload_to ='uploads/authors', default='../static/img/user.svg') 


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    updated_on = models.DateField(auto_now= True)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    description = models.CharField(max_length=300)
    upload = models.ImageField(upload_to ='uploads/post_backgrounds') 
    tags = models.CharField(max_length=25)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    n_views = models.IntegerField(default=0, editable=False)
    n_comments = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Subscribers(models.Model):
    email = models.EmailField(max_length = 254) 
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.email)
