from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import (logout, login)


urlpatterns = [
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    #url(r'^post/new/$', views.loadCounties, name='loadCounties'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),

    url(r'^$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^user/$', views.user_list, name='user_list'),
    url(r'^user/new/$', views.user_new, name='user_new'),
    url(r'^user/(?P<pk>\d+)/edit/$', views.user_edit, name='user_edit'),
    url(r'^user/(?P<pk>\d+)/remove/$', views.user_remove, name='user_remove'),

    url(r'^ajax_load_counties/$', views.loadCounties, name='ajax_load_counties'),
    url(r'^ajax_load_data/$', views.getdetails, name='ajax_load_data'),
    url(r'^get_pdf/(?P<pk>\d+)/$', views.getpdf, name='get_pdf'),

    url(r'^ajax_pagination/$', views.ajaxPagination, name='ajax_pagination'),
    url(r'^ajax_client_data/$', views.ajaxClientData, name='ajax_client_data'),
    
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

]