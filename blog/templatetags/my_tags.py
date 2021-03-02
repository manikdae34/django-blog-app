from django import template
from ..models import Post, Comment
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def modulo_2(num):
    return num % 2


@register.simple_tag
def latest_3_posts():
    posts_3 = Post.objects.filter(status=1).order_by('-created_on')[:3]
    return posts_3


@register.simple_tag
def get_tags():
    tags = set()
    for post in Post.objects.filter(status=1).order_by('-created_on'):
        post_tags = post.tags
        post_tags = [tags.add(tag.lower()) for tag in post_tags.split()]
        print(tags)
    print('\n'*3)
    return tags    


@register.filter
def get_tags_from_post(post, n='all'):
    tags = post.tags.split()
    if n == 'all':
        return tags
    if len(tags) > n:
        tags = tags[:n]
        return tags
    return tags

@register.filter
def get_read_time(content):
    plain_message = strip_tags(content)
    print(plain_message)
    word_count = len(plain_message.split())   
    print('\n'*5)
    print('word_count = ', word_count)
    avg = 200

    minutes = word_count // avg
    seconds = (word_count/avg - minutes)*0.6

    if seconds > 0.3:
        minutes += 1

    if minutes == 0:
        minutes += 1

    return minutes


@register.filter
def get_no_comments(post):
    comments = Comment.objects.filter(post=post)
    print('\n'*5)
    print('number of comments = ', len(comments))
    return len(comments)
