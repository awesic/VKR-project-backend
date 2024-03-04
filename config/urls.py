from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from .yasg import urlpatterns as yasg_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('users.urls')),
    path("", include('directions.urls')),
    path("", include('main.urls')),
]
urlpatterns += yasg_urlpatterns
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
