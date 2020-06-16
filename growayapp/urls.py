"""growayapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.contrib.auth import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^accounts/login/$', views.LoginView, name='login'),
    re_path(r'^accounts/logout/$', views.LogoutView, name='logout'),
    re_path(r'^accounts/password_change/$', views.PasswordChangeView, name='password_change'),
    re_path(r'^accounts/password_change/done/$', views.PasswordChangeDoneView, name='password_change_done'),
    re_path(r'^accounts/password_reset/$', views.PasswordResetView, name='password_reset'),
    re_path(r'^accounts/password_reset/done/$', views.PasswordResetDoneView, name='password_reset_done'),
    re_path(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.PasswordResetConfirmView, name='password_reset_confirm'),
    re_path(r'^accounts/reset/done/$', views.PasswordResetCompleteView, name='password_reset_complete'),
    re_path(r'', include('groway.urls')),
    re_path(r'^select2/', include('django_select2.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
