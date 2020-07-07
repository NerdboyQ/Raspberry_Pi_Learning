"""bots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.piCarDash, name="picar"),
    url(r'^sanity_checks', views.piCarTests, name="piCarTests"),
    url(r'^start_camera',views.startCam, name="startCamera"),
    url(r'^stop_camera',views.stopCam, name="stopCamera"),
    url(r'^picam_feed',views.piCamFeed, name='piCamFeed')
]
