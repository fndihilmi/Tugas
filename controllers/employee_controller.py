from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from models.employee_model import employees

employee_bp = Blueprint("employee_bp", __name__)


def find_employee(employee_id):
    return next((employee for employee in employees if employee["id"] == employee_id), None)


def render_employee_page(employee=None, error=None, status=200, form_values=None):
    return (
        render_template(
            "form.html",
            employees=employees,
            employee=employee,
            error=error,
            form_values=form_values or {},
        ),
        status,
    )


def read_employee_form():
    values = {
        "name": request.form.get("name", "").strip(),
        "position": request.form.get("position", "Staff").strip() or "Staff",
    }
    salary_value = request.form.get("salary", "0")

    if not values["name"]:
        return None, "Nama wajib diisi!", values

    try:
        salary = int(salary_value)
    except ValueError:
        return None, "Gaji harus berupa angka bulat.", values

    if salary < 0:
        return None, "Gaji tidak boleh kurang dari 0.", values

    values["salary"] = salary
    return values, None, values


@employee_bp.route("/")
@employee_bp.route("/employees/new", methods=["GET"])
def list_employees_page():
    return render_employee_page()


@employee_bp.route("/employees", methods=["GET"])
def list_employees():
    return jsonify(employees), 200


@employee_bp.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = find_employee(employee_id)
    if employee is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(employee), 200


@employee_bp.route("/employees/new", methods=["POST"])
def create_employee():
    values, error, form_values = read_employee_form()
    if error:
        return render_employee_page(error=error, status=400, form_values=form_values)

    values["id"] = max((employee["id"] for employee in employees), default=0) + 1
    employees.append(values)
    return redirect(url_for("employee_bp.list_employees_page"))


@employee_bp.route("/employees/<int:employee_id>/edit", methods=["GET"])
def edit_employee(employee_id):
    employee = find_employee(employee_id)
    if employee is None:
        return "Employee tidak ditemukan.", 404
    return render_employee_page(employee=employee)


@employee_bp.route("/employees/<int:employee_id>/edit", methods=["POST"])
def update_employee(employee_id):
    employee = find_employee(employee_id)
    if employee is None:
        return "Employee tidak ditemukan.", 404

    values, error, form_values = read_employee_form()
    if error:
        return render_employee_page(
            employee=employee,
            error=error,
            status=400,
            form_values=form_values,
        )

    employee.update(values)
    return redirect(url_for("employee_bp.list_employees_page"))


@employee_bp.route("/employees/<int:employee_id>/delete", methods=["POST"])
def delete_employee(employee_id):
    employee = find_employee(employee_id)
    if employee is None:
        return jsonify({"error": "Not found"}), 404

    employees.remove(employee)
    return redirect(url_for("employee_bp.list_employees_page"))
