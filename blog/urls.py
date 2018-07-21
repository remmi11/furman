from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    #url(r'^post/new/$', views.loadCounties, name='loadCounties'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'^post/new/$', views.loadCounties, name='ajax_load_counties'),

]