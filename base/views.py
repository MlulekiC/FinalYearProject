from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
        ListView,
        UpdateView, 
        DeleteView,
        View
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.conf import settings
#User = settings.AUTH_USER_MODEL
from . import models as base_models
from . import forms as base_forms
from django.db.models import Q
from users.models import User
from django.http import JsonResponse
from users.models import Town
from django.contrib import messages

from .utilities import create_notification


class PostListView(LoginRequiredMixin, ListView):
    model = base_models.Post
    template_name = "base/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        return base_models.Post.objects.filter(author__municipality = \
            self.request.user.municipality).order_by("-date_posted")

class CommunityRequestPosts(LoginRequiredMixin, ListView):
    model = base_models.CommunityRequestPost
    template_name = "base/community_requests.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        return base_models.CommunityRequestPost.objects.filter(author__municipality = \
            self.request.user.municipality).order_by("-date_posted")

class UserPostListView(LoginRequiredMixin, ListView):
    model = base_models.Post
    template_name = "base/user_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get("username"))
        return base_models.Post.objects.filter(author = user).order_by("-date_posted")

class PostDetailView(LoginRequiredMixin, View):
    context_object_name = 'post'
    def get(self, request, pk, *args ,**kwargs):
        post = base_models.Post.objects.get(pk = pk)
        form = base_forms.CommentForm()

        comments = base_models.Comment.objects.filter(post = post).order_by('-created_on')

        context = {
            "post": post,
            "form": form,
            "comments": comments,
        }
        return render(request, 'base/post_detail.html', context)
    
    def post(self, request, pk, *args, **kwrags):
        post = base_models.Post.objects.get(pk = pk)
        form = base_forms.CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = base_models.Comment.objects.filter(post = post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            "comments": comments,
        }

        return render(request, 'base/post_detail.html', context)


class RequestPostDetailView(LoginRequiredMixin, View):
    context_object_name = 'post'
    def get(self, request, pk, *args ,**kwargs):
        post = base_models.CommunityRequestPost.objects.get(pk = pk)
        form = base_forms.CommentForm()

        comments = base_models.RequestComment.objects.filter(post = post).order_by('-created_on')

        context = {
            "post": post,
            "form": form,
            "comments": comments,
        }
        return render(request, 'base/request_post_detail.html', context)
    
    def post(self, request, pk, *args, **kwrags):
        post = base_models.CommunityRequestPost.objects.get(pk = pk)
        form = base_forms.RequestCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = base_models.RequestComment.objects.filter(post = post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            "comments": comments,
        }

        return render(request, 'base/request_post_detail.html', context)
        

class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = base_forms.PostForm()
        return render(request, 'base/post_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = base_forms.PostForm(request.POST, request.FILES)
        if form.is_valid:
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            create_notification(
                request, 
                to_user = User.objects.filter(municipality=new_post.author.municipality).exclude(username=new_post.author), 
                notification_type = 'post',
                extra_id = new_post.id
            )
            return redirect('post-detail', pk=new_post.id)
        
        return render(request, 'base/post_form.html', {'form': form})


class CreateCommunityRequestPostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = base_forms.RequestPostForm()
        return render(request, 'base/post_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = base_forms.RequestPostForm(request.POST)
        if form.is_valid:
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            create_notification(
                request, 
                to_user = User.objects.filter(municipality=new_post.author.municipality).exclude(username=new_post.author), 
                notification_type = 'post',
                extra_id = new_post.id
            )
            return redirect('request-posts')
        
        return render(request, 'base/post_form.html', {'form': form})



class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = base_models.Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


##################################################
class UpdateCommunityPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = base_models.CommunityRequestPost
    fields = ['title', 'content']
    template_name = 'base/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = base_models.Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class DeleteCommunityPostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = base_models.CommunityRequestPost
    template_name = 'base/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ListThreads(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        threads = base_models.ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        return render(request, 'base/inbox.html', {'threads': threads})

class CreateThread(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = base_forms.ThreadForm()
        users = User.objects.filter(Q(role='STAFF') & Q(municipality=request.user.municipality))

        return render(request, 'base/create_thread.html', {'form': form, 'users': users})

    def post(self, request, *args, **kwargs):
        form = base_forms.ThreadForm(request.POST)
        username = request.POST.get('username')
        try:
            receiver = User.objects.get(username=username)
            if base_models.ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = base_models.ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)

            elif base_models.ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = base_models.ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = base_models.ThreadModel(
                    user = request.user, 
                    receiver = receiver
                )
                thread.save()
                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')


class ThreadView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        form = base_forms.MessageForm()
        thread = base_models.ThreadModel.objects.get(pk=pk)
        message_list = base_models.PersonalRequest.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }
        return render(request, 'base/thread.html', context)


class CreateRequest(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        thread = base_models.ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        message = base_models.PersonalRequest(
            thread = thread,
            sender_user = request.user,
            receiver_user = receiver,
            body = request.POST.get('message')
        )
        message.save()
        """
        create_notification(
                request, 
                to_user = User.objects.get(username=message.receiver_user), 
                notification_type = 'message',
                extra_id = message.id
            )
            """
        return redirect('thread', pk=pk)


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = base_models.Comment
    template_name = 'base/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def notifications(request):
    return render(request, 'base/notifications.html')


class NotificationDetailView(LoginRequiredMixin, View):
    context_object_name = 'notification'
    def get(self, request, pk, *args ,**kwargs):
        notification = base_models.Notification.objects.get(pk = pk)
        notification.is_read = True
        notification.save()
        return render(request, 'base/notification_detail.html', {'notification': notification})


def about(request):
    return render(request, 'base/about.html', {'title': 'About'})


@login_required
def create_alert(request):
    if request.method == "POST":
        user = request.user
        town = base_models.Town.objects.get(name=request.POST['town'])
        message =   request.POST['message']

        alert = base_models.Alert.objects.create(
            author=user,
            location=town,
            content = message
        )
        alert.save()
        create_notification(
                request, 
                to_user = User.objects.filter(Q(town=alert.location) & Q(is_staff=True)).exclude(username=alert.author), 
                notification_type = 'alert',
                extra_id = alert.id
            )
        return redirect('alert-detail', pk=alert.id)
    return render(request, 'alerts/alert_form.html')

class AlertListView(LoginRequiredMixin, ListView):
    model = base_models.Alert
    template_name = "alerts/alerts.html"
    context_object_name = "alerts"
    ordering = ["-created_on"]
    paginate_by = 5

    def get_queryset(self):
        return base_models.Alert.objects.filter(author__municipality = \
            self.request.user.municipality).order_by("-created_on")


class AlertDetailView(LoginRequiredMixin, View):
    context_object_name = 'alert'
    def get(self, request, pk, *args ,**kwargs):
        alert = base_models.Alert.objects.get(pk = pk)
        return render(request, 'alerts/alert_detail.html', {'alert':alert})
    

def get_related_json_town_data(request):
    admin_municipality = request.user.municipality
    obj_models = list(Town.objects.filter(municipality__name=admin_municipality).values())
    return JsonResponse({'data':obj_models})