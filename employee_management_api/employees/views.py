from django.views.generic import TemplateView
from drf_yasg import openapi
from rest_framework import viewsets
from .serializers import EmployeeSerializer, DepartmentSerializer, PerformanceSerializer
from .models import Employee, Department, Performance
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
import json


# Refactored params into a seperate function because manually putting them in the header looked ugly
def employee_filter_params():
    return [
        openapi.Parameter(
            "department",
            openapi.IN_QUERY,
            description="Department ID",
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            "date_of_joining",
            openapi.IN_QUERY,
            description="Date of Jonining",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "department__department_name",
            openapi.IN_QUERY,
            description="Department Name",
            type=openapi.TYPE_STRING,
        ),
    ]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["department", "date_of_joining", "department__department_name"]

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


class ChartView(TemplateView):
    template_name = "chart.html"

    def get_context_data(self, **kwargs):
        context = {}

        departments = Department.objects.all()
        context["departments"] = [dept.department_name for dept in departments]
        context["employees_per_department"] = [
            dept.employee_set.count() for dept in departments
        ]
        context["attendance"] = "hihihi"

        # make info json safe
        context = {field: json.dumps(context[field]) for field in context}

        return context
