from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from employees import views
from employee_portal import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.user_redirect, name='user_redirect_root'),
    path('admin/', admin.site.urls),
    path('', include('employees.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
