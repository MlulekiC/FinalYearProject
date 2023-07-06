from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),

    path('post/new/', views.CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # Alerts
    path('alerts', views.AlertListView.as_view(), name='alerts'),
    path('alert/new/', views.create_alert, name='create-alert'),
    path('towns-json/', views.get_related_json_town_data, name='admin-towns-json'),
    path('alert/<int:pk>/', views.AlertDetailView.as_view(), name='alert-detail'),

    path('request-post/<int:pk>/', views.RequestPostDetailView.as_view(), name='request-post-detail'),

    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='post-delete'),

    path('community-post/<int:pk>/update/', views.UpdateCommunityPostView.as_view(), name='community-post-update'),
    path('community-post/<int:pk>/delete/', views.DeleteCommunityPostView.as_view(), name='community-post-delete'),

    path('request-posts/', views.CommunityRequestPosts.as_view(), name='request-posts'),
    path('create-request-post/', views.CreateCommunityRequestPostView.as_view(), name='create-request-post'),

    path('user/<str:username>/', views.UserPostListView.as_view(), name='user-posts'),
    # Threading
    path('inbox/', views.ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread', views.CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', views.CreateRequest.as_view(), name='create-message'),

    path('about/', views.about, name='about'),

    path('notification/', views.notifications , name='notifications'),

    path('notification/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),

    path('post/<int:post_pk>/comment/delete/<int:pk>/', views.DeleteCommentView.as_view(), name='comment-delete'),
]