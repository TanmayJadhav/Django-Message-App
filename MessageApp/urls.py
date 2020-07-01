
from django.contrib import admin
from django.conf.urls import url,include

urlpatterns = [
    url(r'^',include('message_app.urls')),
    url(r'^admin/',admin.site.urls),
]
