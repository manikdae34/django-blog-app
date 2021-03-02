from .models import Comment, Post
from django import forms
from tinymce import TinyMCE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# class PostForm(forms.ModelForm):
#     content = forms.CharField(
#         widget=TinyMCE(attrs={
#             'required': False,
#             'cols': 30,
#             'rows': 10
#         }))

#     class Meta:
#         model = Post
#         fields = '__all__'
