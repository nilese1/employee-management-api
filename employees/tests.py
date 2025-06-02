from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Department, Employee, Performance
import datetime


class DepartmentCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass")
        self.client.login(username="tester", password="testpass")

    def test_create_department(self):
        url = reverse("department-list")
        data = {"department_name": "Finance"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 1)

    def test_retrieve_department(self):
        dept = Department.objects.create(department_name="IT")
        url = reverse("department-detail", args=[dept.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["department_name"], "IT")

    def test_update_department(self):
        dept = Department.objects.create(department_name="Sales")
        url = reverse("department-detail", args=[dept.id])
        response = self.client.put(url, {"department_name": "Marketing"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["department_name"], "Marketing")

    def test_delete_department(self):
        dept = Department.objects.create(department_name="Support")
        url = reverse("department-detail", args=[dept.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Department.objects.filter(id=dept.id).exists())


class EmployeeCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass")
        self.client.login(username="tester", password="testpass")
        self.department = Department.objects.create(department_name="Legal")

    def test_create_employee(self):
        url = reverse("employee-list")
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "phone_number": "1234567890",
            "address": "1 Law Street",
            "date_of_joining": "2023-01-01",
            "department": self.department.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)

    def test_retrieve_employee(self):
        emp = Employee.objects.create(
            first_name="Jake",
            last_name="Smith",
            email="jake@example.com",
            phone_number="9876543210",
            address="2 Court Ave",
            date_of_joining="2022-10-01",
            department=self.department,
        )
        url = reverse("employee-detail", args=[emp.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "jake@example.com")

    def test_update_employee(self):
        emp = Employee.objects.create(
            first_name="Laura",
            last_name="Knight",
            email="laura@example.com",
            phone_number="5551234567",
            address="3 Legal Blvd",
            date_of_joining="2021-06-15",
            department=self.department,
        )
        url = reverse("employee-detail", args=[emp.id])
        new_data = {
            "first_name": "Laura",
            "last_name": "Knight",
            "email": "laura.k@example.com",
            "phone_number": "5551234567",
            "address": "3 Legal Blvd",
            "date_of_joining": "2021-06-15",
            "department": self.department.id,
        }
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "laura.k@example.com")

    def test_delete_employee(self):
        emp = Employee.objects.create(
            first_name="Tom",
            last_name="Holland",
            email="tom@example.com",
            phone_number="4445556666",
            address="4 Alley",
            date_of_joining="2020-04-10",
            department=self.department,
        )
        url = reverse("employee-detail", args=[emp.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=emp.id).exists())


class PerformanceCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass")
        self.client.login(username="tester", password="testpass")
        self.department = Department.objects.create(department_name="R&D")
        self.employee = Employee.objects.create(
            first_name="Sam",
            last_name="Lee",
            email="sam@example.com",
            phone_number="1112223333",
            address="5 Innovation Dr",
            date_of_joining="2023-03-03",
            department=self.department,
        )

    def test_create_performance(self):
        url = reverse("performance-list")
        data = {
            "employee": self.employee.id,
            "rating": 5,
            "review_date": "2024-01-01",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performance.objects.count(), 1)

    def test_retrieve_performance(self):
        perf = Performance.objects.create(
            employee=self.employee, rating=4, review_date="2023-12-01"
        )
        url = reverse("performance-detail", args=[perf.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 4)

    def test_update_performance(self):
        perf = Performance.objects.create(
            employee=self.employee, rating=2, review_date="2023-05-01"
        )
        url = reverse("performance-detail", args=[perf.id])
        data = {"employee": self.employee.id, "rating": 3, "review_date": "2023-05-01"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 3)

    def test_delete_performance(self):
        perf = Performance.objects.create(
            employee=self.employee, rating=1, review_date="2022-10-10"
        )
        url = reverse("performance-detail", args=[perf.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Performance.objects.filter(id=perf.id).exists())
