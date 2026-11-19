from rest_framework.routers import DefaultRouter
from .views import ProgressViewSet, LearningSessionViewSet

router = DefaultRouter()

router.register("progress", ProgressViewSet, basename="progress")
router.register(
    "learning-sessions",
    LearningSessionViewSet,
    basename="learning-session"
)

urlpatterns = router.urls