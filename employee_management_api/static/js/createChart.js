function createAttendanceChart(canvas, attendance) {}

function createEmployeeChart(canvas, employees_per_department, departments) {
  new Chart(canvas, {
    type: "pie",
    data: {
      labels: departments,
      datasets: [
        {
          label: "Employees per Department",
          data: employees_per_department,
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
            "#FF9F40",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "right",
        },
      },
    },
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const employee_canvas = document
    .getElementById("Employees per Departent Pie Chart")
    .getContext("2d");

  const attendance_canvas = document
    .getElementById("Monthly Attendance Bar Chart")
    .getContext("2d");

  const data = JSON.parse(document.getElementById("chart-data").textContent);

  createAttendanceChart(attendance_canvas, data.attendance);
  createEmployeeChart(
    employee_canvas,
    data.employees_per_department,
    data.departments,
  );
});
