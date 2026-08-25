from rest_framework.routers import DefaultRouter
from faqs.views import FAQViewSet

router = DefaultRouter()
router.register("faqs", FAQViewSet, basename="faqs")
urlpatterns = router.urls
