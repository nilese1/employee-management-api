import random
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models.functions.datetime import timezone
from employees.models import Employee, Department

from faker import Faker


class Command(BaseCommand):
    RELEVANT_DEPARTMENTS = ("Sales", "Human Resources", "Finance", "Marketing")
    help = "Seed the database with a default of 10 records, use --count to specify how many to add"

    def create_employee(self):
        fake = Faker()

        dept_name = random.choice(self.RELEVANT_DEPARTMENTS)
        department = Department.objects.get_or_create(department_name=dept_name)

        Employee.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone_number=fake.phone_number(),
            address=fake.address(),
            date_of_joining=fake.date(),
            department=department[0],
        )

        self.stdout.write("John deployed!")

    def handle(self, *args, **options):
        count = options["count"]
        clear = options["clear"]

        if clear:
            Employee.objects.all().delete()

        for _ in range(count):
            try:
                self.create_employee()
            except IntegrityError:
                self.stderr.write(f"Something went wrong... skipping employee {i}")

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of records to create"
        )
        parser.add_argument(
            "--clear", action="store_true", help="Clear existing data first"
        )
