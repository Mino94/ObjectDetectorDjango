from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import url,include
import machine.views

# router = routers.DefaultRouter()
# router.register(r'version', VersionViewSet)


urlpatterns = [
    url(r'admin/', admin.site.urls),

    path('', machine.views.index, name="index"),
    path('video_feed', machine.views.video_feed, name="video_feed"),
    path('machine/new', machine.views.new, name = "new"),

    # path('/new', machine.views.post, name='new_video'),

    
    
]
