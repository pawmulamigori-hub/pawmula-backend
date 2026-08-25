from rest_framework.routers import DefaultRouter
from mining.views import MiningStageViewSet, MinerProfileViewSet

router = DefaultRouter()
router.register("mining-stages", MiningStageViewSet, basename="mining-stages")
router.register("miner-profiles", MinerProfileViewSet, basename="miner-profiles")
urlpatterns = router.urls
