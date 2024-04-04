
from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Bidding System API",
        default_version='v1',
        description="Bidding System API",
       
    ),
    public=True,
 )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/',
        include([
            path('api/', include('base.urls')),
            path('swagger/schema',schema_view.with_ui('swagger', cache_timeout=0)),
        ]) 
    )
]
