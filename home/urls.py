from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name='index'),
    path("home", views.home, name='home'),
    # path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("queries", views.queries, name='queries'),
    path("QnA", views.QnA, name='QnA'),
    path("mcq", views.mcq, name='mcq'),
    path("TnF", views.TnF, name='TnF'),
    path("fill", views.fill, name='fill'),
    path("combine", views.combine, name='combine'),
    path("history", views.history, name='history'),
    path("login", views.login, name='login'),
    path("signup", views.signup, name='signup'),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
