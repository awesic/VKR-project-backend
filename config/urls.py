from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from .yasg import urlpatterns as yasg_urlpatterns

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/", include('users.urls')),
    path("api/", include('directions.urls')),
    path("api/", include('main.urls')),
]
urlpatterns += yasg_urlpatterns
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
