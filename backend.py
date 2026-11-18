from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import IntegrityError

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university"
    )


@app.route("/all-students", methods=["GET"])
def get_all_students():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return jsonify(students), 200
    finally:
        cursor.close()
        db.close()


@app.route("/detail-students/<nim>", methods=["GET"])
def get_student_detail(nim):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM students WHERE nim = %s", (nim,))
        student = cursor.fetchone()
        if student is None:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student), 200
    finally:
        cursor.close()
        db.close()


@app.route("/add-student", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Body must be valid JSON"}), 400

    required = ["nim", "name", "major"]
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (nim, name, major) VALUES (%s, %s, %s)",
            (data["nim"], data["name"], data["major"])
        )
        db.commit()
        return jsonify({"message": "Student added successfully"}), 201
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "NIM already exists"}), 409
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)