
from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'^$',views.signup,name='signup_page'),
    url(r'logout',views.logout,name='logout_page'),
    url(r'done',views.send_message,name='send_message'),     
]