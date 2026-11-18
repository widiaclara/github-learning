from flask import Flask, jsonify,request
app = Flask(__name__)
students = [
        {"NIM": 1, "NAME" : "KENNY", "MAJOR": "IT"},
          {"NIM": 2, "NAME" : "GABRIE;", "MAJOR": "IS"},
        
]

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)

@app.route("/inputStudents", methods=["POST"])
def add_students():
    new_students = request.get_json()
    students.append(new_students)
    return jsonify(students)

@app.route("/home")
def home():
    return "welcome to my first flask app"

if __name__ == "__main__":
    app.run(debug=True)
