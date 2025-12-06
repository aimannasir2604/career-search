from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import os
import sqlite3
from datetime import datetime


app = Flask(__name__)
app.secret_key = "dev-secret-key"  # needed for flash messages in profile editing


COUNSELORS = {
    "sj": {
        "id": "sj",
        "initials": "SJ",
        "name": "Dr. Sarah Johnson",
        "role": "PhD in Career Counseling",
        "specialization": "Career Guidance & Planning",
        "availability": "Mon–Fri, 9 AM – 5 PM",
        "experience": "15+ years experience",
    },
    "mc": {
        "id": "mc",
        "initials": "MC",
        "name": "Dr. Michael Chen",
        "role": "MSc Psychology",
        "specialization": "Student Development",
        "availability": "Tue–Sat, 10 AM – 6 PM",
        "experience": "12+ years experience",
    },
    "er": {
        "id": "er",
        "initials": "ER",
        "name": "Dr. Emily Rodriguez",
        "role": "PhD in Educational Psychology",
        "specialization": "Academic & Career Counseling",
        "availability": "Mon–Thu, 2 PM – 8 PM",
        "experience": "10+ years experience",
    },
    "jw": {
        "id": "jw",
        "initials": "JW",
        "name": "Dr. James Williams",
        "role": "MBA & Career Coach Certification",
        "specialization": "Industry Insights & Planning",
        "availability": "Wed–Sun, 11 AM – 7 PM",
        "experience": "8+ years experience",
    },
}


USER_PROFILE = {
    "initials": "SE",
    "full_name": "Sara ejaz",
    "father_name": "muhammad ejaz",
    "age": "19",
    "student_class": "10",
    "address": "Not provided",
    "student_id": "ID-xx92-bazum-622-210",
    "current_gpa": "3.40",
    "quiz_completed": True,
    "personality": {
        "analytical": 20,
        "creative": 30,
        "social": 40,
        "practical": 10,
    },
    "recommended_careers": ["Teacher", "Counselor", "Human Resources", "Social Worker"],
    "appointments": [
        {
            "counselor": "Dr. Sarah Johnson",
            "date": "Saturday, November 29, 2025 at 8:00 PM",
            "mode": "Audio Call",
            "status": "Confirmed",
        }
    ],
}


def get_db_connection():
    db_path = os.path.join(app.instance_path, "career_search.db")
    os.makedirs(app.instance_path, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_admin_user():
    """Create admin table and default admin user if they don't exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            category TEXT,
            trait1 TEXT,
            trait2 TEXT,
            trait3 TEXT,
            trait4 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS gpa_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            total_marks REAL NOT NULL,
            obtained_marks REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS consultants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            counselor_id TEXT UNIQUE NOT NULL,
            initials TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            specialization TEXT NOT NULL,
            availability TEXT NOT NULL,
            experience TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analytical_score INTEGER NOT NULL,
            creative_score INTEGER NOT NULL,
            social_score INTEGER NOT NULL,
            practical_score INTEGER NOT NULL,
            dominant_trait TEXT NOT NULL,
            time_taken INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            counselor_id TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            mode TEXT NOT NULL,
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(counselor_id, appointment_date, appointment_time)
        )
        """
    )
    # Migrate existing COUNSELORS to database if table is empty
    cur.execute("SELECT COUNT(*) FROM consultants")
    if cur.fetchone()[0] == 0:
        default_consultants = [
            ("sj", "SJ", "Dr. Sarah Johnson", "PhD in Career Counseling", 
             "Career Guidance & Planning", "Mon–Fri, 9 AM – 5 PM", "15+ years experience"),
            ("mc", "MC", "Dr. Michael Chen", "MSc Psychology", 
             "Student Development", "Tue–Sat, 10 AM – 6 PM", "12+ years experience"),
            ("er", "ER", "Dr. Emily Rodriguez", "PhD in Educational Psychology", 
             "Academic & Career Counseling", "Mon–Thu, 2 PM – 8 PM", "10+ years experience"),
            ("jw", "JW", "Dr. James Williams", "MBA & Career Coach Certification", 
             "Industry Insights & Planning", "Wed–Sun, 11 AM – 7 PM", "8+ years experience"),
        ]
        cur.executemany(
            """
            INSERT INTO consultants 
            (counselor_id, initials, name, role, specialization, availability, experience)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            default_consultants
        )
    cur.execute(
        """
        INSERT OR IGNORE INTO admin (email, password)
        VALUES (?, ?)
        """,
        ("admin202@gmail.com", "admin202"),
    )
    # Insert default questions if table is empty
    cur.execute("SELECT COUNT(*) FROM quiz_questions")
    if cur.fetchone()[0] == 0:
        default_questions = [
            ("How do you prefer to solve problems?", 
             "Through logical analysis and data", "By thinking outside the box",
             "Working with others to find solutions", "Using hands-on practical methods",
             "Engineering", "analytical", "creative", "social", "practical"),
            ("Which activity sounds most enjoyable to you?",
             "Designing or creating something new", "Leading a team project",
             "Conducting experiments or research", "Fixing or building physical things",
             "General", "creative", "social", "analytical", "practical"),
            ("In group projects, you usually:",
             "Organize tasks and keep everyone on track", "Come up with unique ideas and approaches",
             "Handle the technical or detailed work", "Do the hands-on implementation",
             "General", "social", "creative", "analytical", "practical"),
        ]
        cur.executemany(
            """
            INSERT INTO quiz_questions 
            (question_text, option1, option2, option3, option4, category, trait1, trait2, trait3, trait4)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            default_questions
        )
    conn.commit()
    conn.close()


# Initialize database on startup
ensure_admin_user()


@app.route("/")
def index():
    # Show splash screen first
    return render_template("splash.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: add real authentication later
        # For now, just redirect back to login or to a homepage if you have one
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # TODO: save new user to the database and add validation
        # For now, simply redirect to the home dashboard after "registration"
        return redirect(url_for("home"))
    return render_template("signup.html")


@app.route("/home")
def home():
    # Placeholder user name until real auth is added
    user_name = request.args.get("name", "Student")
    return render_template("home.html", user_name=user_name)


@app.route("/gpa")
def gpa():
    return render_template("gpa.html")


@app.route("/api/gpa/subjects", methods=["GET"])
def get_gpa_subjects():
    """Get all GPA subjects"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, subject_name, total_marks, obtained_marks FROM gpa_subjects ORDER BY id")
    subjects = []
    for row in cur.fetchall():
        subjects.append({
            "id": row["id"],
            "subject_name": row["subject_name"],
            "total_marks": row["total_marks"],
            "obtained_marks": row["obtained_marks"]
        })
    conn.close()
    return jsonify(subjects)


@app.route("/api/gpa/subjects", methods=["POST"])
def create_gpa_subject():
    """Create a new GPA subject"""
    data = request.get_json()
    subject_name = data.get("subject_name", "").strip()
    total_marks = float(data.get("total_marks", 0))
    obtained_marks = float(data.get("obtained_marks", 0))
    
    if not subject_name or total_marks <= 0:
        return jsonify({"error": "Invalid data"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO gpa_subjects (subject_name, total_marks, obtained_marks) VALUES (?, ?, ?)",
        (subject_name, total_marks, obtained_marks)
    )
    conn.commit()
    subject_id = cur.lastrowid
    conn.close()
    
    return jsonify({
        "id": subject_id,
        "subject_name": subject_name,
        "total_marks": total_marks,
        "obtained_marks": obtained_marks
    }), 201


@app.route("/api/gpa/subjects/<int:subject_id>", methods=["PUT"])
def update_gpa_subject(subject_id):
    """Update an existing GPA subject"""
    data = request.get_json()
    subject_name = data.get("subject_name", "").strip()
    total_marks = float(data.get("total_marks", 0))
    obtained_marks = float(data.get("obtained_marks", 0))
    
    if not subject_name or total_marks <= 0:
        return jsonify({"error": "Invalid data"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE gpa_subjects SET subject_name = ?, total_marks = ?, obtained_marks = ? WHERE id = ?",
        (subject_name, total_marks, obtained_marks, subject_id)
    )
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    
    if not updated:
        return jsonify({"error": "Subject not found"}), 404
    
    return jsonify({
        "id": subject_id,
        "subject_name": subject_name,
        "total_marks": total_marks,
        "obtained_marks": obtained_marks
    })


@app.route("/api/gpa/subjects/<int:subject_id>", methods=["DELETE"])
def delete_gpa_subject(subject_id):
    """Delete a GPA subject"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM gpa_subjects WHERE id = ?", (subject_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    
    if not deleted:
        return jsonify({"error": "Subject not found"}), 404
    
    return jsonify({"message": "Subject deleted successfully"}), 200


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/consultation")
def consultation():
    # Load consultants from database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT counselor_id, initials, name, role, specialization, availability, experience FROM consultants ORDER BY id")
    consultants = {}
    for row in cur.fetchall():
        consultants[row["counselor_id"]] = {
            "id": row["counselor_id"],
            "initials": row["initials"],
            "name": row["name"],
            "role": row["role"],
            "specialization": row["specialization"],
            "availability": row["availability"],
            "experience": row["experience"],
        }
    conn.close()
    # Fallback to COUNSELORS if database is empty
    if not consultants:
        consultants = COUNSELORS
    return render_template("consultation.html", counselors=consultants)


@app.route("/consultation/book/<counselor_id>", methods=["GET", "POST"])
def book_appointment(counselor_id):
    # Get all consultants for the template
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT counselor_id, initials, name, role, specialization, availability, experience FROM consultants ORDER BY id")
    all_consultants = {}
    for r in cur.fetchall():
        all_consultants[r["counselor_id"]] = {
            "id": r["counselor_id"],
            "initials": r["initials"],
            "name": r["name"],
            "role": r["role"],
            "specialization": r["specialization"],
            "availability": r["availability"],
            "experience": r["experience"],
        }
    conn.close()
    if not all_consultants:
        all_consultants = COUNSELORS
    
    # Handle multi-counsellor selection
    if counselor_id == "multi":
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        if request.method == "POST":
            counselor_ids = request.form.getlist("counselor_ids")
            if not counselor_ids:
                return redirect(url_for("consultation"))
            
            selected_counselors = []
            for cid in counselor_ids:
                if cid in all_consultants:
                    selected_counselors.append(all_consultants[cid])
            
            # Check if this is a confirmation submission
            if request.form.get("confirm") == "true":
                # Process bookings
                bookings = []
                comments = request.form.get("comments", "").strip()
                conn = get_db_connection()
                cur = conn.cursor()
                
                # Check for time slot conflicts
                time_slots = {}
                for cid in counselor_ids:
                    date_key = request.form.get(f"date_{cid}")
                    time_key = request.form.get(f"time_{cid}")
                    if date_key and time_key:
                        slot_key = f"{date_key}_{time_key}"
                        if slot_key in time_slots:
                            conn.close()
                            flash("Error: Multiple counselors cannot be booked for the same time slot.", "error")
                            return render_template(
                                "book_appointment.html",
                                counselors=all_consultants,
                                selected_counselors=selected_counselors,
                                selected=None,
                                confirmed=False,
                                today_date=today_date,
                            )
                        time_slots[slot_key] = cid
                
                # Save bookings to database
                for cid in counselor_ids:
                    date_val = request.form.get(f"date_{cid}")
                    time_val = request.form.get(f"time_{cid}")
                    mode_val = request.form.get(f"mode_{cid}", "video")
                    
                    if date_val and time_val:
                        try:
                            cur.execute(
                                """
                                INSERT INTO appointments (counselor_id, appointment_date, appointment_time, mode, comments)
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                (cid, date_val, time_val, mode_val, comments)
                            )
                            conn.commit()
                            
                            # Format date for display
                            date_obj = datetime.strptime(date_val, "%Y-%m-%d")
                            date_formatted = date_obj.strftime("%A, %B %d, %Y")
                            
                            bookings.append({
                                "counselor": all_consultants[cid],
                                "date": date_val,
                                "date_formatted": date_formatted,
                                "time": time_val,
                                "mode": mode_val
                            })
                        except sqlite3.IntegrityError:
                            conn.rollback()
                            flash(f"Error: Time slot {time_val} on {date_val} is already booked for {all_consultants[cid]['name']}.", "error")
                            conn.close()
                            return render_template(
                                "book_appointment.html",
                                counselors=all_consultants,
                                selected_counselors=selected_counselors,
                                selected=None,
                                confirmed=False,
                                today_date=today_date,
                            )
                
                conn.close()
                
                if bookings:
                    return render_template(
                        "book_appointment.html",
                        counselors=all_consultants,
                        bookings=bookings,
                        comments=comments,
                        confirmed=True,
                        today_date=today_date,
                    )
            
            # Show booking form with selected counsellors
            return render_template(
                "book_appointment.html",
                counselors=all_consultants,
                selected_counselors=selected_counselors,
                selected=None,
                confirmed=False,
                today_date=today_date,
            )
        else:
            return redirect(url_for("consultation"))
    
    # Single counsellor selection (backward compatibility)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT counselor_id, initials, name, role, specialization, availability, experience FROM consultants WHERE counselor_id = ?", (counselor_id,))
    row = cur.fetchone()
    conn.close()
    
    if row:
        counselor = {
            "id": row["counselor_id"],
            "initials": row["initials"],
            "name": row["name"],
            "role": row["role"],
            "specialization": row["specialization"],
            "availability": row["availability"],
            "experience": row["experience"],
        }
    else:
        # Fallback to COUNSELORS
        counselor = COUNSELORS.get(counselor_id, COUNSELORS.get("sj", {}))
    
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    if request.method == "POST":
        if request.form.get("confirm") == "true":
            # Process booking
            selected_date = request.form.get("date")
            selected_time = request.form.get("time")
            mode = request.form.get("mode", "video")
            comments = request.form.get("comments", "").strip()
            
            # Save to database
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute(
                    """
                    INSERT INTO appointments (counselor_id, appointment_date, appointment_time, mode, comments)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (counselor_id, selected_date, selected_time, mode, comments)
                )
                conn.commit()
                conn.close()
                
                # Format date for display
                date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
                date_formatted = date_obj.strftime("%A, %B %d, %Y")
                
                bookings = [{
                    "counselor": counselor,
                    "date": selected_date,
                    "date_formatted": date_formatted,
                    "time": selected_time,
                    "mode": mode
                }]
                
                return render_template(
                    "book_appointment.html",
                    counselors=all_consultants,
                    bookings=bookings,
                    comments=comments,
                    confirmed=True,
                    today_date=today_date,
                )
            except sqlite3.IntegrityError:
                conn.rollback()
                conn.close()
                flash(f"Error: Time slot {selected_time} on {selected_date} is already booked for {counselor['name']}.", "error")
                return render_template(
                    "book_appointment.html",
                    counselors=all_consultants,
                    selected=counselor,
                    selected_counselors=None,
                    confirmed=False,
                    today_date=today_date,
                )

    return render_template(
        "book_appointment.html",
        counselors=all_consultants,
        selected=counselor,
        selected_counselors=None,
        confirmed=False,
        today_date=today_date,
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        USER_PROFILE["full_name"] = request.form.get("full_name", USER_PROFILE["full_name"])
        USER_PROFILE["father_name"] = request.form.get(
            "father_name", USER_PROFILE.get("father_name", "")
        )
        USER_PROFILE["age"] = request.form.get("age", USER_PROFILE["age"])
        USER_PROFILE["student_class"] = request.form.get(
            "student_class", USER_PROFILE["student_class"]
        )
        USER_PROFILE["address"] = request.form.get("address", USER_PROFILE["address"])
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", profile=USER_PROFILE)


@app.route("/quiz-settings/login", methods=["GET", "POST"])
def quiz_settings_login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE email = ? AND password = ?", (email, password)
        )
        row = cur.fetchone()
        conn.close()

        if row:
            session["is_admin"] = True
            session["admin_email"] = email
            return redirect(url_for("quiz_settings"))
        else:
            error = "Invalid admin credentials."

    return render_template("quiz_settings_login.html", error=error)


@app.route("/quiz-settings", methods=["GET", "POST"])
def quiz_settings():
    if not session.get("is_admin"):
        return redirect(url_for("quiz_settings_login"))

    conn = get_db_connection()
    message = None
    
    if request.method == "POST":
        question_text = request.form.get("question_text", "").strip()
        option1 = request.form.get("option1", "").strip()
        option2 = request.form.get("option2", "").strip()
        option3 = request.form.get("option3", "").strip()
        option4 = request.form.get("option4", "").strip()
        category = request.form.get("category", "").strip()
        
        if question_text and option1 and option2 and option3 and option4:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO quiz_questions 
                (question_text, option1, option2, option3, option4, category, trait1, trait2, trait3, trait4)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (question_text, option1, option2, option3, option4, category, 
                 "analytical", "creative", "social", "practical")
            )
            conn.commit()
            message = "Quiz question saved successfully!"
        else:
            message = "Please fill in all fields."
    
    # Get all questions for the sidebar
    cur = conn.cursor()
    cur.execute("SELECT id, question_text FROM quiz_questions ORDER BY id")
    questions = cur.fetchall()
    conn.close()
    
    return render_template("quiz_settings.html", message=message, questions=questions)


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    session.pop("admin_email", None)
    return redirect(url_for("home"))


# Consultant Management API Routes
@app.route("/api/consultants", methods=["GET"])
def get_consultants():
    """Get all consultants"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, counselor_id, initials, name, role, specialization, availability, experience FROM consultants ORDER BY id")
    consultants = []
    for row in cur.fetchall():
        consultants.append({
            "id": row["id"],
            "counselor_id": row["counselor_id"],
            "initials": row["initials"],
            "name": row["name"],
            "role": row["role"],
            "specialization": row["specialization"],
            "availability": row["availability"],
            "experience": row["experience"]
        })
    conn.close()
    return jsonify(consultants)


@app.route("/api/consultants", methods=["POST"])
def create_consultant():
    """Create a new consultant"""
    data = request.get_json()
    counselor_id = data.get("counselor_id", "").strip().lower()
    initials = data.get("initials", "").strip().upper()
    name = data.get("name", "").strip()
    role = data.get("role", "").strip()
    specialization = data.get("specialization", "").strip()
    availability = data.get("availability", "").strip()
    experience = data.get("experience", "").strip()
    
    if not all([counselor_id, initials, name, role, specialization, availability, experience]):
        return jsonify({"error": "All fields are required"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO consultants (counselor_id, initials, name, role, specialization, availability, experience) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (counselor_id, initials, name, role, specialization, availability, experience)
        )
        conn.commit()
        consultant_id = cur.lastrowid
        conn.close()
        
        return jsonify({
            "id": consultant_id,
            "counselor_id": counselor_id,
            "initials": initials,
            "name": name,
            "role": role,
            "specialization": specialization,
            "availability": availability,
            "experience": experience
        }), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Consultant ID already exists"}), 400


@app.route("/api/consultants/<int:consultant_id>", methods=["PUT"])
def update_consultant(consultant_id):
    """Update an existing consultant"""
    data = request.get_json()
    counselor_id = data.get("counselor_id", "").strip().lower()
    initials = data.get("initials", "").strip().upper()
    name = data.get("name", "").strip()
    role = data.get("role", "").strip()
    specialization = data.get("specialization", "").strip()
    availability = data.get("availability", "").strip()
    experience = data.get("experience", "").strip()
    
    if not all([counselor_id, initials, name, role, specialization, availability, experience]):
        return jsonify({"error": "All fields are required"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if counselor_id is being changed and if it conflicts
    cur.execute("SELECT counselor_id FROM consultants WHERE id = ?", (consultant_id,))
    existing = cur.fetchone()
    if existing and existing["counselor_id"] != counselor_id:
        cur.execute("SELECT id FROM consultants WHERE counselor_id = ?", (counselor_id,))
        if cur.fetchone():
            conn.close()
            return jsonify({"error": "Consultant ID already exists"}), 400
    
    cur.execute(
        "UPDATE consultants SET counselor_id = ?, initials = ?, name = ?, role = ?, specialization = ?, availability = ?, experience = ? WHERE id = ?",
        (counselor_id, initials, name, role, specialization, availability, experience, consultant_id)
    )
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    
    if not updated:
        return jsonify({"error": "Consultant not found"}), 404
    
    return jsonify({
        "id": consultant_id,
        "counselor_id": counselor_id,
        "initials": initials,
        "name": name,
        "role": role,
        "specialization": specialization,
        "availability": availability,
        "experience": experience
    })


@app.route("/api/consultants/<int:consultant_id>", methods=["DELETE"])
def delete_consultant(consultant_id):
    """Delete a consultant"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM consultants WHERE id = ?", (consultant_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    
    if not deleted:
        return jsonify({"error": "Consultant not found"}), 404
    
    return jsonify({"message": "Consultant deleted successfully"}), 200


@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    """Submit quiz results"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["analytical_score", "creative_score", "social_score", "practical_score", "dominant_trait", "time_taken", "total_questions"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate scores are integers
        scores = {
            "analytical": int(data["analytical_score"]),
            "creative": int(data["creative_score"]),
            "social": int(data["social_score"]),
            "practical": int(data["practical_score"])
        }
        
        # Validate dominant trait
        if data["dominant_trait"] not in ["analytical", "creative", "social", "practical"]:
            return jsonify({"error": "Invalid dominant trait"}), 400
        
        # Save to database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO quiz_submissions 
            (analytical_score, creative_score, social_score, practical_score, dominant_trait, time_taken, total_questions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                scores["analytical"],
                scores["creative"],
                scores["social"],
                scores["practical"],
                data["dominant_trait"],
                int(data["time_taken"]),
                int(data["total_questions"])
            )
        )
        conn.commit()
        submission_id = cur.lastrowid
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Quiz results submitted successfully",
            "submission_id": submission_id
        }), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error submitting quiz: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)


