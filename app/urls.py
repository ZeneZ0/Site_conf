from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from pc_builder.api import (
    ProcessorViewSet, VideoCardViewSet, MotherboardViewSet,
    ComputerBuildViewSet, UserFavoriteViewSet, UserViewSet
)

router = DefaultRouter()
router.register(r'processors', ProcessorViewSet)
router.register(r'videocards', VideoCardViewSet)
router.register(r'motherboards', MotherboardViewSet)
router.register(r'builds', ComputerBuildViewSet)
router.register(r'favorites', UserFavoriteViewSet)
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)