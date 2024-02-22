from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from .yasg import urlpatterns as yasg_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include('users.urls')),
    path("api/v1/", include('directions.urls')),
    path("api/v1/", include('main.urls')),
]
urlpatterns += yasg_urlpatterns
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
