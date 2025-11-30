from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tasks.views import index

urlpatterns = [
    path('', index, name='home'),          # 👈 root serves index.html
    path('admin/', admin.site.urls),
    path('api/tasks/', include('tasks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "frontend")
