from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os

# --- App ko setup karna ---
app = Flask(__name__)
auth = HTTPBasicAuth() 

# === USERNAME AUR PASSWORD YAHAN SET HAI ===
users = {
    "Faizan": "faizan@01"
}

# === 1. PEHLE DATABASE KO CONFIGURE KAREIN ===
# Yeh nayi line hai (poora path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/shami03/Academy-poject/students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# === 2. AB DATABASE KO APP SE CONNECT KAREIN ===
db = SQLAlchemy(app)


# --- Database Model (Student) ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    current_class = db.Column(db.String(50), nullable=False)
    school_name = db.Column(db.String(200), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    whatsapp = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    aadhaar = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    course_interest = db.Column(db.String(50), nullable=False)
    requirements = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Student {self.student_name}>'

# === PASSWORD CHECK KARNE WALA FUNCTION ===
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# --- Website ke Routes (Pages) ---

# === 1. Homepage (Form wala page) ===
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_student = Student(
            student_name=request.form['student_name'],
            dob=request.form['dob'],
            gender=request.form['gender'],
            current_class=request.form['current_class'],
            school_name=request.form['school_name'],
            father_name=request.form['father_name'],
            mother_name=request.form['mother_name'],
            contact=request.form['contact'],
            whatsapp=request.form['whatsapp'],
            email=request.form['email'],
            aadhaar=request.form['aadhaar'],
            address=request.form['address'],
            course_interest=request.form['course_interest'],
            requirements=request.form['requirements']
        )
        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('success'))
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return "<h2>Error: Data save nahi hua.</h2>"
    return render_template('index.html')

# === 2. Success Page (Registration ke baad) ===
@app.route('/success')
def success():
    return '''
        <html>
            <head><title>Success</title><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
            <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                <h1>Registration Successful!</h1><p>Aapka data humare paas save ho gaya hai.</p>
                <a href="/">Go back to Homepage</a>
            </body>
        </html>
    '''

# === 3. Admin Page (Password Protected) ===
@app.route('/admin')
@auth.login_required
def admin_page():
    try:
        all_students = Student.query.all()
        return render_template('admin.html', students=all_students)
    except Exception as e:
        print(f"Error fetching students: {e}")
        return "<h2>Error: Students ka data nahi mila.</h2>"


# === 4. NAYA DELETE ROUTE (YEH ADD HUA HAI) ===
@app.route('/delete/<int:id>')
@auth.login_required  # Ise bhi password protected rakha hai
def delete_student(id):
    # Student ko uski ID se dhoondhna
    student_to_delete = Student.query.get(id)
    
    if student_to_delete:
        try:
            db.session.delete(student_to_delete)
            db.session.commit()
        except Exception as e:
            print(f"Error deleting: {e}")
            db.session.rollback()
            
    # Delete karne ke baad, waapas admin page par bhej dena
    return redirect(url_for('admin_page'))


# --- Server ko run karne ke liye ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
