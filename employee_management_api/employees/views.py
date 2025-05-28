from django.shortcuts import render
from drf_yasg import openapi
from rest_framework import viewsets
from .serializers import EmployeeSerializer, DepartmentSerializer, PerformanceSerializer
from .models import Employee, Department, Performance
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema


# Refactored params into a seperate function because manually putting them in the header looked ugly
def employee_filter_params():
    return [
        openapi.Parameter(
            "department",
            openapi.IN_QUERY,
            description="Department",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "date_of_joining",
            openapi.IN_QUERY,
            description="Date of Jonining",
            type=openapi.TYPE_STRING,
        ),
    ]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # filter by department and date joined
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["department", "date_of_joining"]

    @swagger_auto_schema(
        operation_description="Retrieve a list of employees with filters",
        manual_parameters=employee_filter_params(),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
