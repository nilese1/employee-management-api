from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EmployeeViewSet,
    DepartmentViewSet,
    PerformanceViewSet,
    ChartView,
    RegisterView,
    logout_redirect,
)

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet)
router.register(r"departments", DepartmentViewSet)
router.register(r"performance", PerformanceViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("charts/", ChartView.as_view(), name="charts"),
    path("accounts/logout/", logout_redirect, name="logout-redirect"),
]
