from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    template_name = 'libreria/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/'
        return '/tienda/'


def logout_view(request):
    logout(request)
    return redirect('/login/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('libreria.urls')),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),  # ← cambiado
    path('tienda/', include('libreria.urls_tienda')),
    path('', include('libreria.views_html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)