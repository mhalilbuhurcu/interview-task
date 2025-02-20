from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InfluencerViewSet, SocialMediaViewSet


router = DefaultRouter()
router.register(r'influencers', InfluencerViewSet, basename='influencers')
router.register(r'social_media', SocialMediaViewSet, basename='social_media')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # API root view
    path('', router.get_api_root_view(), name='api-root'),
]
