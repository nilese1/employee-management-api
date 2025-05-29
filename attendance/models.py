from django.db import models
from employees.models import Employee


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.get_status_display()}"

    class Meta:
        unique_together = ["employee", "date"]
        ordering = ["-date", "employee__first_name", "employee__last_name"]
