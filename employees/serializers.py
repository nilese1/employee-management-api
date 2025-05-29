from .models import Employee, Performance, Department
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
