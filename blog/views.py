from django.views import generic
from .models import Post, Subscribers, Comment
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
import random
from django.db.models import Q
import math


def error_404(request, exception):
    data = {}
    response = render(request, 'blog/404.html', data)
    return response

def error_500(request, *args, **argv):
    return render(request, 'blog/404.html')

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/blog.html'
    paginate_by = 4

    def get_queryset(self): # new
        query = self.request.GET.get('q', '')
        print('\n')
        query = ' '.join(query.split())

        if query == None or query == '':
            object_list = Post.objects.filter(status=1).order_by('-created_on')
        
        else:
            print('query = ', query)
            object_list = []
            for que in query.split():

                pos_list = Post.objects.filter(
                    Q(title__icontains=que) | Q(description__icontains=que) | Q(tags__icontains=que),
                    status=1
                ).order_by('-created_on')
                
                object_list.extend(pos_list)
                print(object_list)

        return list(set(object_list))


def post_detail(request, slug):
    template_name = 'blog/post.html'
    print('\n'*3)
    print(request.GET.get('email_status', 0))

    email_status = request.GET.get('email_status', 0)
    comment_status = request.GET.get('comment_status', 0)

    post = get_object_or_404(Post, slug=slug, status=1)
    post.n_views += 1
    post.save()

    comments = Comment.objects.filter(post=post).order_by('-created_on')

    return render(request, template_name, {'post': post, 
                                            'email_status': email_status, 
                                            'comments': comments,
                                            'comment_status': comment_status
                                            })



def comment(request):
    next = request.POST.get('next')
    post = Post.objects.get(slug=next.split('/')[2])
    
    post.n_comments += 1
    post.save()

    comment_body = request.POST.get('comment-body')
    comment_name = request.POST.get('comment-name')
    comment_email = request.POST.get('comment-email', None)

    print('\n'*5)
    print(comment_name)
    print(comment_email)
    print(comment_body)

    if comment_email is not None:
        print('inside if comment_email condition !')
        if not Subscribers.objects.filter(email=comment_email).exists():
            print('email does not exist !')
            subscriber = Subscribers.objects.create(email=comment_email)
            subscriber.save()
            print('email saved !')


    c = Comment.objects.create(name=comment_name, email=comment_email, post=post, body=comment_body)
    c.save()
    
    next += '?comment_status=posted#tags'

    return HttpResponseRedirect(next)


def subscribe(request):
    if request.method == 'POST':
        subs_email = request.POST.get('subs_email', None)
        next = request.POST.get('next', '/')

        if subs_email is not None:
            if Subscribers.objects.filter(email=subs_email).exists():
                next += '?email_status=exists#subscribe'
            else:
                subscriber = Subscribers.objects.create(email=subs_email)
                subscriber.save()
                next += '?email_status=added#subscribe'

        print(next)

    return HttpResponseRedirect(next)


def index(request):

    # post ranking system to detect popular posts of all time.

    posts = list(Post.objects.filter(status=1))

    view_comment_score = []
    post_list = []

    if len(posts) != 0:
        max_view = max(post.n_views for post in posts)
        max_comment = max(post.n_comments for post in posts)

        for i, post in enumerate(posts):
            print('\n'*2)
            print(post.title)
            score = (0.3+math.log10(10+post.n_views) / math.log10(10+max_view)) + (0.7+math.log10(10+post.n_comments) / math.log10(10+max_comment))
            print(score)
            view_comment_score.append(score)

        ranking_dict = dict(zip(posts, view_comment_score))
        ranking_dict = {k: v for k, v in sorted(ranking_dict.items(), key=lambda item: item[1], reverse=True)}

        print(ranking_dict)
        
        post_list = list(ranking_dict.keys())[:3]
        print(post_list)

    return render(request, 'blog/index.html', {'post_list' : post_list})

    
