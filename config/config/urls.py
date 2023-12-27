from django.contrib import admin
from django.urls import path, include  # Обязательный импорт include
from django.conf import settings
from django.conf.urls.static import static  # Обязательный импорт static
from photoapp.views import DownloadImageView
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main app
    path('', include('photoapp.urls')),
    path('users/', include('users.urls')),
    path('photo/', include('photoapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

