from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import tweet_detail_view, tweet_list_view, TweetDetailView, TweetListView, tweet_create_view, tweet_update_view, delete_view
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url="/")),
    path('search/', tweet_list_view, name='list'),
    path('<int:pk>', tweet_detail_view, name='detail'),
    path('create/', tweet_create_view, name='create'),
    path('<int:pk>/edit/', tweet_update_view, name='update'),
    path('<int:pk>/delete/', delete_view, name='delete'),
    # CLASS BASED VIEWS
    # path('<int:pk>', TweetDetailView.as_view(), name='detail'),
    # path('', TweetListView.as_view(), name='list'),
]
