from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

from .yasg import urlpatterns as yasg_urlpatterns

urlpatterns = [
    path("api/admin/", admin.site.urls),
    
    # user urls
    path("api/", include('apps.users.urls')),
    path("api/", include('apps.main.urls')),
    
    # urls to fetch university departments
    path("api/", include('apps.directions.urls')),
    
    # JWT token
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# URL for documentation
urlpatterns += yasg_urlpatterns

from django.conf.urls.static import static
from django.conf import settings

# if settings.DEBUG:
    # urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
