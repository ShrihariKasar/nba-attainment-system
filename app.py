import os
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import pdfkit

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_secret_key")

# ✅ Config
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"
DB_FILE = "data.db"
ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ Ensure required folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# ✅ PDFKit config (adjust path if wkhtmltopdf installed elsewhere)
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = None
if os.path.exists(WKHTMLTOPDF_PATH):
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# ✅ Init Database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attainment_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student TEXT,
            average_marks REAL,
            attainment_level TEXT,
            direct_attainment REAL,
            indirect_attainment REAL,
            final_attainment REAL,
            co_mapping TEXT,
            po_mapping TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ✅ File type check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')

    if 'file' not in request.files:
        flash("No file part", "error")
        return redirect(url_for('upload_file'))

    file = request.files['file']

    if file.filename == '':
        flash("No selected file", "error")
        return redirect(url_for('upload_file'))

    if not allowed_file(file.filename):
        flash("Invalid file type. Please upload an Excel (.xlsx) file.", "error")
        return redirect(url_for('upload_file'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        df = pd.read_excel(filepath)
        df.columns = df.columns.str.strip()

        required_columns = {
            'Student', 'Average Marks', 'Attainment Level',
            'Direct Attainment (%)', 'Indirect Attainment (%)', 'Final Attainment (%)',
            'CO1', 'CO2', 'CO3', 'CO4', 'CO5', 'CO6',
            'PO1', 'PO2', 'PO3', 'PO4', 'PO5', 'PO6'
        }
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            flash(f"Invalid file format. Missing columns: {', '.join(missing_columns)}", "error")
            return redirect(url_for('upload_file'))

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        co_columns = [f'CO{i}' for i in range(1, 7)]
        po_columns = [f'PO{i}' for i in range(1, 7)]

        for _, row in df.iterrows():
            co_mapping = {col: row[col] for col in co_columns if pd.notna(row[col])}
            po_mapping = {col: row[col] for col in po_columns if pd.notna(row[col])}

            cursor.execute("""
                INSERT INTO attainment_data 
                (student, average_marks, attainment_level, direct_attainment, indirect_attainment, final_attainment, co_mapping, po_mapping) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['Student'], row['Average Marks'], row['Attainment Level'],
                row['Direct Attainment (%)'], row['Indirect Attainment (%)'], row['Final Attainment (%)'],
                str(co_mapping), str(po_mapping)
            ))

        conn.commit()
        conn.close()

        # ✅ Generate graphs & reports
        generate_graphs(df)
        report_path = generate_report(df, file.filename)
        pdf_report_path = generate_pdf_report(df, file.filename)

        # ✅ Prepare data for template
        data_list = df.to_dict(orient="records")
        attainment_counts = df["Attainment Level"].value_counts().to_dict()
        co_po_counts = {col: df[col].sum() for col in co_columns + po_columns if col in df.columns}

        return render_template(
            'result.html',
            data=data_list,
            filename=file.filename,
            report_path=os.path.basename(report_path) if report_path else None,
            pdf_report_path=os.path.basename(pdf_report_path) if pdf_report_path else None,
            attainment_counts=attainment_counts,
            co_po_counts=co_po_counts
        )

    except Exception as e:
        flash(f"Processing failed: {str(e)}", "error")
        return redirect(url_for('upload_file'))

# ✅ Graphs
def generate_graphs(df):
    if "Attainment Level" not in df.columns:
        return
    plt.figure(figsize=(8, 5))
    df["Attainment Level"].value_counts().plot(kind='bar', color=['red', 'orange', 'green'])
    plt.xlabel("Attainment Level")
    plt.ylabel("Count")
    plt.title("Attainment Level Distribution")
    plt.savefig(os.path.join(STATIC_FOLDER, "attainment_bar.png"))
    plt.close()

# ✅ Excel Report
def generate_report(df, filename):
    report_filename = f"processed_{filename}"
    report_path = os.path.join(UPLOAD_FOLDER, report_filename)
    df.to_excel(report_path, index=False)
    return report_path

# ✅ PDF Report
def generate_pdf_report(df, filename):
    if not config:
        print("⚠ wkhtmltopdf not found, skipping PDF generation.")
        return None
    html_content = df.to_html()
    pdf_filename = f"report_{filename.split('.')[0]}.pdf"
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    try:
        pdfkit.from_string(html_content, pdf_path, configuration=config)
        return pdf_path
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return None

# ✅ Download Route
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# ✅ Contact Route
@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)