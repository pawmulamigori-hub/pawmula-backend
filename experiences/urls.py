from rest_framework.routers import DefaultRouter
from experiences.views import ExperienceViewSet

router = DefaultRouter()
router.register("experiences", ExperienceViewSet, basename="experiences")
urlpatterns = router.urls
