from django.conf.urls import patterns, include, url
from django.contrib import admin

from gnsite import views
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^latest$', views.IndexView.as_view(latest=True), name='latest'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^create/$', views.PostCreateView.as_view(), name='post_create'),
    url(r'^(?P<pk>\d+)/update/$', views.PostUpdateView.as_view(), name='post_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(), name='post_delete'),
    url(r'^(?P<pk>\d+)/upvote/$', views.upvote, name='upvote'),
    url(r'^(?P<pk>\d+)/comment/$', views.addcomment, name='addcomment'),
    url(r'^(?P<pk>\d+)/comment/edit$', views.CommentUpdateView.as_view(), name='comment_update'),

    url(r'^accounts/profile$', views.ProfileView.as_view(), name='profile'),
    url(r'^accounts/profile/(?P<username>\w+)$', views.ProfileView.as_view(), name='profile'),
    url(r'^tos$', TemplateView.as_view(template_name="site/tos.html"), name='tos'),
)
