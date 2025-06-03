from rest_framework import viewsets

from employees.permissions import IsAdminOrReadOnly

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows attendances to be viewed or edited.

    Provides standard CRUD operations on the Attendance model.
    """

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrReadOnly]
