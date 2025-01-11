from django.urls import path
from py_project import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_view, name='upload'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('visualization/', views.visualization_view, name='visualization'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Add this line
