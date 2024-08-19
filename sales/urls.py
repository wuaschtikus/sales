"""sales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from msgconv.views.index import IndexView

urlpatterns = [
    path(r'^$', IndexView.as_view(), name='index'),
    path('', include('users.urls')),
    path('', include('msgconv.urls')),
    path('convert/', include('msgconv.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # required by allauth
    path('login/', TemplateView.as_view(template_name='account/login.html'), name='login'),
]

# error sites
handler404 = TemplateView.as_view(template_name='error/404.html')
handler500 = TemplateView.as_view(template_name='error/500.html')

if settings.DEBUG:
    # set index site for webpage
    urlpatterns = [
        path('', TemplateView.as_view(template_name='msgconv/index.html'), name='index'),
    ] + urlpatterns
    
    # required for static assets in debug mode
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # enables debug toolbar
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    
else:
    urlpatterns = [
        path('', TemplateView.as_view(template_name='base/index.html'), name='index'),
    ] + urlpatterns

   



