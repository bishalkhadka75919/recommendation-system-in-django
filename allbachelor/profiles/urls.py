from . import views
from django.conf.urls import url, include
from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'profiles'


urlpatterns = [
    # path('accounts/', include('profiles.accounts.urls', namespace='accounts')),
    path('profiles/<slug:profile_slug>/change-password', views.change_password, name="change-password"),
    path('profiles/<slug:profile_slug>/edit', views.edit_profile, name="edit-profile"),
    path('profiles/<slug:profile_slug>/', views.profile, name="profile"),
    path('', views.profiles, name="profiles"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




