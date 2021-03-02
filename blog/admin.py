from django.contrib import admin
from .models import Post, Comment, User, Subscribers
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib.sites.models import Site
import os


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'profile_img',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on', 'n_views', 'n_comments')
    list_filter = ("status",)
    search_fields = ['title', 'content', 'description', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['mail_posts']

    class Media:
        js = ('tinyinject.js',)
        css = {
             'all': ('tinycss.css',)
        }

    def mail_posts(self, request, queryset):
        datatuple = list()
        
        recipients = Subscribers.objects.all()
        recipients = [recipient.email for recipient in recipients]
        print(recipients)

        for post in queryset:
            subject = post.title
            text = post.description

            extra_posts = Post.objects.all()
            extra_2_posts = random.choices(extra_posts, k=2)

            content = strip_tags(post.content)

            current_site = Site.objects.get_current()

            html = render_to_string('blog/mail_template.html', {'post': post, 'content': content, 'extra_2_posts': extra_2_posts, 'site': current_site})
            
            complete_info = (subject, text, html, None, recipients)
            datatuple.append(complete_info)


        def send_mass_html_mail(datatuple, fail_silently=True, user=None, password=None, 
                                connection=None):
            """
            Given a datatuple of (subject, text_content, html_content, from_email,
            recipient_list), sends each message to each recipient list. Returns the
            number of emails sent.

            If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
            If auth_user and auth_password are set, they're used to log in.
            If auth_user is None, the EMAIL_HOST_USER setting is used.
            If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

            """
            connection = connection or get_connection(
                username=user, password=password, fail_silently=fail_silently)
            messages = []
            for subject, text, html, from_email, recipient in datatuple:
                message = EmailMultiAlternatives(subject, text, from_email, recipient)
                message.attach_alternative(html, 'text/html')
                messages.append(message)
            return connection.send_messages(messages)

        print(send_mass_html_mail(datatuple))

        return render(request, 'blog/mail_template.html', {'post': post, 'content': content, 'extra_2_posts': extra_2_posts})


admin.site.register(Post, PostAdmin)


@admin.register(Comment)            # another way to register a model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')
    search_fields = ('email',)
admin.site.register(Subscribers, SubscribersAdmin)
