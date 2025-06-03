from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.views.generic.base import HttpResponseRedirect
from drf_yasg import openapi
from rest_framework import viewsets

from attendance.models import Attendance
from employee_management_api.settings import LOGOUT_REDIRECT_URL
from employees.permissions import IsAdminOrReadOnly
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
    """
    API endpoint that allows employees to be viewed or edited.

    Provides standard CRUD operations on the Employee model.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["department", "date_of_joining", "department__department_name"]

    @swagger_auto_schema(
        operation_description="Retrieve a list of employees with filters",
        manual_parameters=employee_filter_params(),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows departments to be viewed or edited.

    Provides standard CRUD operations on the Department model.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]


class PerformanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows performances to be viewed or edited.

    Provides standard CRUD operations on the Performance model.
    """

    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAdminOrReadOnly]


class ChartView(TemplateView):
    """
    View responsible for handling chart data
    """

    template_name = "chart.html"

    def get_attendance_graph_data(self, month, year):
        """
        Returns the attendance data given a month and a year
        returns a tuple of arrays (labels, data) to be used in graphing
        applications
        """
        attendance_for_month = Attendance.objects.filter(
            date__month=month, date__year=year
        )

        status_names = []
        status_counts = []
        for status in Attendance.STATUS_CHOICES:
            status_names.append(status[0])
            current_status_count = attendance_for_month.filter(status=status[0]).count()
            status_counts.append(current_status_count)

        return (status_names, status_counts)

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
        attendance_labels, attendance_data = self.get_attendance_graph_data(month, year)

        data["attendance_labels"] = attendance_labels
        data["attendance_data"] = attendance_data

        # make info json safe
        data = {field: json.dumps(data[field]) for field in data}

        # put json safe data back into context
        for field in data:
            context[field] = data[field]

        return context


# standard logout redirect thingy
def logout_redirect(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
