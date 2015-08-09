from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('gnsite.urls')),
    url(r'^accounts/', include('registration_custombackend.urls')),
)
