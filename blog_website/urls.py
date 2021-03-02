from django.urls import path, re_path, include
# from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [

    path('admin/', admin.site.urls),    # admin URLs
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'blog.views.error_404'
handler500 = 'blog.views.error_500'
