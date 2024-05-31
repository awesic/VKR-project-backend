from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as yasg_urlpatterns

urlpatterns = [
    path("api/admin/", admin.site.urls),
    
    # user urls
    path("api/", include('apps.users.urls')),
    path("api/", include('apps.main.urls')),
    
    path("api/forgejo/", include('apps.forgejo.urls')),
    
    # urls to fetch university departments
    path("api/", include('apps.directions.urls')),
]

# URL for documentation
urlpatterns += yasg_urlpatterns

from django.conf.urls.static import static
from django.conf import settings

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
