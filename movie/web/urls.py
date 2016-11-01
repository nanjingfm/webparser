from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^baidu/showtop1000', views.showtop1000, name="baidu_showtop1000"),
]