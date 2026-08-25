from rest_framework.routers import DefaultRouter
from testimonials.views import TestimonialViewSet

router = DefaultRouter()
router.register("testimonials", TestimonialViewSet, basename="testimonials")
urlpatterns = router.urls
