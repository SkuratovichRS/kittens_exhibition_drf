from rest_framework.routers import DefaultRouter

from exhibition.views import KittenViewSet, BreedViewSet, UserViewSet, RatingViewSet

router = DefaultRouter()

router.register('kittens', KittenViewSet, basename='kittens')
router.register('breeds', BreedViewSet, basename='breeds')
router.register('users', UserViewSet, basename='users')
router.register('ratings', RatingViewSet, basename='ratings')

urlpatterns = router.urls
