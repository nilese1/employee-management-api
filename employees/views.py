from django.views.generic import TemplateView
from drf_yasg import openapi
from rest_framework import viewsets

from attendance.models import Attendance
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
        context = super().get_context_data(**kwargs)
        data = {}

        departments = Department.objects.all()
        data["departments"] = [dept.department_name for dept in departments]
        data["employees_per_department"] = [
            dept.employee_set.count() for dept in departments
        ]

        # For now get current year and month, maybe add month selection later
        year = self.request.GET.get("year")
        month = self.request.GET.get("month")

        # TODO: refactor into seperate function
        attendance_for_month = Attendance.objects.filter(
            date__month=month, date__year=year
        )
        status_names = []
        status_counts = []
        for status in Attendance.STATUS_CHOICES:
            status_names.append(status[0])
            current_status_count = attendance_for_month.filter(status=status[0]).count()
            status_counts.append(current_status_count)

        data["attendance_labels"] = status_names
        data["attendance_data"] = status_counts

        # make info json safe
        data = {field: json.dumps(data[field]) for field in data}

        # put json safe data back into context
        for field in data:
            context[field] = data[field]

        return context
