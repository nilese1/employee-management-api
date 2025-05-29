from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, DepartmentViewSet, PerformanceViewSet, ChartView

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet)
router.register(r"departments", DepartmentViewSet)
router.register(r"performance", PerformanceViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("charts/", ChartView.as_view(), name="charts"),
]
