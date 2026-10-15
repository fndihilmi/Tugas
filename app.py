from flask import Flask

from controllers.employee_controller import employee_bp

app = Flask(__name__)
app.register_blueprint(employee_bp)


if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
