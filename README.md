# Employee Management API

> RESTful API powered by Django REST Framework, documented with Swagger (`drf-yasg`), containerized with Docker.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/nilese1/employee-management-api.git
cd employee-management-api
```

---

### 2. Setup Environment Variables
Copy the example environment file and edit as needed:
```bash
cp example.env .env
```
> Fill .env with your database credentials or any other required settings

---

### 3. Build and start with Docker

```bash
docker-compose up --build
```

This will:
- Build your app image
- Start the web server and database containers (PostgreSQL by default)

---

### 4. Run management commands

Perform database migrations and create an administrator
```bash
docker-compose exec python-app python manage.py migrate
docker-compose exec python-app python manage.py createsuperuser
```

> (Optional) Seed the database with random Employees and Attendances
```bash
docker-compose exec python-app python manage.py seed_employees --count [count] --clear
docker-compose exec python-app python manage.py seed_attendance --count [count] --clear
```

---

### 5. Watch for code changes (Dev only)

```bash
docker compose up --watch
```

## 🔗 API Endpoints
| Path           | Description            |
|----------------|------------------------|
| `/api/`        | API root               |
| `/swagger/`    | Swagger UI Documentation             |
| `/admin/`      | Django admin panel     |
| `/charts/`     | Visualized dashboard of data|
