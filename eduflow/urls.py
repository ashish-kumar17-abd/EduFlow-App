from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Keep this only for Django default admin

    path('adminpanel/', include('adminpanel.urls')),  # ✅ Custom admin dashboard
    path('auth/', include('authentication.urls')),
    path('', include('pages.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('attendance/', include('attendance.urls')),
]


# ✅ For profile images & uploaded media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
