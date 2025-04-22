import sqlite3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

# Importing extraction functions
from data_extracter import extract_text_from_image, extract_text_from_pdf, extract_text_from_txt

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# DB path
DB_PATH = 'courses.db'

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!", "status": "success"})

@app.route('/upload_course_data', methods=['POST'])
def upload_course_data():
    try:
        # --- REQUIRED FIELDS ---
        required_fields = ['course_code', 'course_name', 'university', 'group', 'branch', 'semester']
        missing_fields = [field for field in required_fields if not request.form.get(field)]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        course_code = request.form.get('course_code')
        course_name = request.form.get('course_name')
        university = request.form.get('university')
        group = request.form.get('group')
        branch = request.form.get('branch')
        semester = request.form.get('semester')

        # --- SYLLABUS VALIDATION ---
        syllabus_file = request.files.get('syllabus_file')
        syllabus_type = request.form.get('syllabus_file_type')

        if not syllabus_file or not syllabus_type:
            return jsonify({
                "error": "Syllabus file and syllabus_file_type are required"
            }), 400

        # Save syllabus file
        filename = secure_filename(syllabus_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        syllabus_file.save(filepath)

        # Extract syllabus text
        if syllabus_type == 'pdf':
            syllabus_text = extract_text_from_pdf(filepath)
        elif syllabus_type == 'txt':
            syllabus_text = extract_text_from_txt(filepath)
        elif syllabus_type == 'image':
            syllabus_text = extract_text_from_image(filepath)
        else:
            return jsonify({"error": "Unsupported syllabus_file_type"}), 400

        # --- INSERT COURSE INTO DB ---
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO courses (course_code, course_name, university, course_group, branch, semester, syllabus_text)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (course_code, course_name, university, group, branch, semester, syllabus_text))

        course_id = cursor.lastrowid

        # --- MATERIALS SECTION ---
        material_files = request.files.getlist('material_files')
        material_type = request.form.get('material_file_type')
        material_texts = []

        if material_files:
            if not material_type:
                return jsonify({
                    "error": "material_file_type is required when material_files are provided"
                }), 400

            for file in material_files:
                if file:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)

                    # Extract based on type
                    if material_type == 'pdf':
                        text = extract_text_from_pdf(filepath)
                    elif material_type == 'txt':
                        text = extract_text_from_txt(filepath)
                    elif material_type == 'image':
                        text = extract_text_from_image(filepath)
                    else:
                        return jsonify({"error": f"Unsupported material_file_type: {material_type}"}), 400

                    # Save to DB
                    cursor.execute('''
                        INSERT INTO materials (course_code, file_name, extracted_text)
                        VALUES (?, ?, ?)
                    ''', (course_code, filename, text))

                    material_texts.append({
                        "file_name": filename,
                        "extracted_text": text
                    })

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Course data uploaded and saved successfully.",
            "course_id": course_id,
            "course_data": {
                "course_code": course_code,
                "course_name": course_name,
                "university": university,
                "group": group,
                "branch": branch,
                "semester": semester,
            },
            "syllabus_text": syllabus_text,
            "materials": material_texts
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
