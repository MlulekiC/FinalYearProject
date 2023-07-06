from django import forms
from .models import Comment, Post, CommunityRequestPost, Alert, RequestComment
from users.models import Municipalitie

# The original Municipality Post form
class PostForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))

    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'image', 'content']

# Community-member Request Post form
class RequestPostForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))

    class Meta:
        model = CommunityRequestPost
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Leave A Comment...'}
        ))

    class Meta:
        model = Comment
        fields = ['content']

class RequestCommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Leave A Comment...'}
        ))

    class Meta:
        model = RequestComment
        fields = ['content']

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)
    #fields = ['username']

class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=500)

class AlertForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))
    
    class Meta:
        model = Alert
        fields = ['location', 'content']