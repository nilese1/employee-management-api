from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EmployeeSerializer, DepartmentSerializer, PerformanceSerializer
from .models import Employee, Department, Performance
from django_filters.rest_framework import DjangoFilterBackend


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # filter by department and date joined
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["department", "date_of_joining"]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
