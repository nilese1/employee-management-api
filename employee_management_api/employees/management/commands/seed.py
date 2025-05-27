import random
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models.functions.datetime import timezone
from employees.models import Employee, Department


class Command(BaseCommand):
    RELEVANT_DEPARTMENTS = ("Sales", "Human Resources", "Finance", "Marketing")
    help = "Seed the database with a default of 10 records, use --count to specify how many to add"

    def create_employee(self, index):
        dept_name = random.choice(self.RELEVANT_DEPARTMENTS)
        department = Department.objects.get_or_create(department_name=dept_name)

        Employee.objects.create(
            first_name=f"fname{index}",
            last_name=f"lname{index}",
            email=f"email{index}@email.com",
            phone_number=f"{index}",
            address=f"{index} street, New York, New York",
            date_of_joining=timezone.now(),
            department=department[0],
        )

        self.stdout.write("John deployed!")

    def handle(self, *args, **options):
        count = options["count"]
        clear = options["clear"]

        if clear:
            Employee.objects.all().delete()

        for i in range(count):
            try:
                self.create_employee(i)
            except IntegrityError:
                self.stderr.write(f"Something went wrong... skipping employee {i}")

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of records to create"
        )
        parser.add_argument(
            "--clear", action="store_true", help="Clear existing data first"
        )
