
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'user/(?P<user_id>[0-9]+)/cube/(?P<cube_id>[0-9]+)/content/(?P<content_id>[0-9]+)', views.deleteContentFromCube),
    url(r'user/(?P<user_id>[0-9]+)/cube/(?P<cube_id>[0-9]+)/content', views.addContentToCube),
    url(r'user/(?P<user_id>[0-9]+)/cube/(?P<cube_id>[0-9]+)/share', views.shareCube),
    url(r'user/(?P<user_id>[0-9]+)/cube/(?P<cube_id>[0-9]+)', views.deleteCube),
    url(r'^user/(?P<user_id>[0-9]+)/cube', views.createGetCube),
    url(r'^user/(?P<user_id>[0-9]+)/content/(?P<content_id>[0-9]+)/share', views.shareContent),
    url(r'^user/(?P<user_id>[0-9]+)/content', views.createGetContent),
    url(r'^user', views.createUser),
    #url(r'^delete', views.deleteAll)
    ]




