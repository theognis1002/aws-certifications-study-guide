from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("staff/", admin.site.urls),
    path("", include("content.urls")),
    path("", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "users.views.error403"
handler404 = "users.views.error404"
handler500 = "users.views.error500"

admin.site.site_header = "AWS Certifications Administration"
