from django.urls import path
from py_project import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.myapp)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)