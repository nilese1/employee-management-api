from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models.functions.datetime import timezone
import random

from employees.models import Employee
from attendance.models import Attendance
from faker import Faker


class Command(BaseCommand):
    help = "Seed the database with fake attendance records (make sure that employees are seeded first)"

    def handle(self, *args, **options):
        fake = Faker()

        count = options["count"]
        clear = options["clear"]

        if clear:
            Attendance.objects.all().delete()

        for _ in range(count):
            Attendance.objects.create(
                employee=Employee.objects.order_by("?").first(),
                date=fake.date(),
                status=random.choice(Attendance.STATUS_CHOICES)[0],
            )

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of records to create"
        )
        parser.add_argument(
            "--clear", action="store_true", help="Clear existing data first"
        )
