# NBA Attainment System

A **web-based NBA Attainment Calculation System** built with **Flask**, **SQLite/MySQL** (configurable), and modern front-end (HTML/CSS/JS).
This system helps educators and administrators compute, visualize and export course attainment results (CO/PO mapping) according to NBA standards.

---

## 🔖 Short description

A lightweight tool for uploading student marks (Excel), calculating direct/indirect/final attainments, classifying attainment levels (High/Medium/Low), visualizing distributions, and exporting reports (Excel/PDF).

---

## 🚀 Features

* Upload Excel files with student marks and CO/PO mappings.
* Automatic calculation of:

  * Direct attainment (%)
  * Indirect attainment (%)
  * Final attainment (%)
* Color-coded classification: **High / Medium / Low**
* Data preview table + interactive charts (Chart.js)
* Export processed report as Excel and PDF
* Simple user-facing pages: Home / Upload / Results / Contact
* Extensible: add role-based auth, notifications, advanced analytics

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite (default) or MySQL (configurable)
* **Frontend:** HTML, CSS (custom / Tailwind/Bootstrap optional), JavaScript, Chart.js
* **Reporting:** pdfkit / wkhtmltopdf (for PDF export)
* **Data:** pandas for Excel processing

---

## 📁 Project structure (suggested)

```
nba-attainment-system/
├── app.py                      # Main Flask application
├── config.py                   # Configuration (DB paths, secrets)
├── requirements.txt            # Python dependencies
├── database.sql                # Example DB schema (optional)
├── templates/                  # Jinja2 HTML templates
│   ├── base.html
│   ├── home.html
│   ├── upload.html
│   ├── results.html
│   ├── contact.html
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
├── uploads/                    # Uploaded files & generated reports
├── utils/
│   ├── reports.py              # generate Excel / PDF helpers
│   └── processing.py           # data processing functions
└── README.md
```

---

## ⚙️ Installation (local)

> **Note:** instructions assume Python 3.8+ and wkhtmltopdf installed for PDF generation (optional).

1. **Clone the repository**

   ```bash
   git clone https://github.com/ShrihariKasar/nba-attainment-system.git
   cd nba-attainment-system
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   # Linux / macOS
   source venv/bin/activate
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # Windows (cmd)
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Install wkhtmltopdf** for PDF export and set path in `config.py` or environment variable:

   * Windows: download installer and note install path (e.g. `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`)
   * Linux: `sudo apt install wkhtmltopdf` (or use distro package manager)

5. **Initialize database (SQLite example)**

   ```bash
   # If using SQLite (default)
   python -c "from utils import init_db; init_db()"
   ```

   Or run `database.sql` in your MySQL instance if you prefer MySQL:

   ```sql
   CREATE DATABASE nba_system;
   USE nba_system;
   SOURCE database.sql;
   ```

6. **Start the app**

   ```bash
   # for local development
   flask run
   # or
   python app.py
   ```

7. **Open your browser**

   ```
   http://127.0.0.1:5000
   ```

---

## 📥 Expected Excel input format

The uploaded Excel should contain a header row with columns similar to:

| Student | Average Marks | Attainment Level | Direct Attainment (%) | Indirect Attainment (%) | Final Attainment (%) | CO1 | CO2 | CO3 | CO4 | CO5 | CO6 | PO1 | PO2 | PO3 | PO4 | PO5 | PO6 |
| ------- | ------------- | ---------------- | --------------------- | ----------------------- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

* Column names are case-insensitive but recommended to match exactly.
* CO/PO columns can be numeric weights (0.0–1.0) or mapping flags.

---

## 📊 Usage / Flow

1. Visit **Upload** page.
2. Select an `.xlsx` file and press **Upload & Process**.
3. App reads file with pandas, validates headers, computes attainment metrics.
4. Processed table and charts are shown on the **Results** page.
5. Download Excel/PDF report from results page links.

---

## 🧩 Helper utilities

* `utils/processing.py` — data cleaning & calculation functions:

  * normalize headers
  * fill NA values
  * compute direct/indirect/final attainment
  * determine attainment level (High/Medium/Low)

* `utils/reports.py` — save processed DataFrame to Excel, generate HTML for pdfkit, and create PDF.

---

## ✅ Example: compute attainment (pseudo)

```python
# final_attainment = (direct_attainment + indirect_attainment) / 2
df['Final Attainment (%)'] = (df['Direct Attainment (%)'] + df['Indirect Attainment (%)']) / 2
# Example threshold: >=60 High, >=40 Medium, else Low
df['Attainment Level'] = df['Final Attainment (%)'].apply(lambda v: 'High' if v >= 60 else ('Medium' if v >= 40 else 'Low'))
```

Adjust thresholds to match your NBA criteria.

---

## 🔒 Environment & config

Create a `.env` or `config.py` containing:

```env
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///data.db   # or mysql+pymysql://user:pass@host/dbname
WKHTMLTOPDF_PATH=/usr/local/bin/wkhtmltopdf
```

---

## 🧪 Testing / Debugging tips

* Print `df.columns.tolist()` after reading Excel to confirm column names.
* Normalize header names:

  ```python
  df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
  ```
* Use `df.fillna('')` before converting to JSON/templates.

---

## 📦 requirements.txt (fixed)

Use this content in your `requirements.txt`. This list is cleaned up (no duplicates) and keeps compatible packages for reading/writing Excel and web deployment.

```
Flask>=2.0
pandas>=1.4
openpyxl>=3.0
numpy>=1.22
python-dotenv>=0.20
pdfkit>=1.0
Jinja2>=3.0
Werkzeug>=2.0
gunicorn>=20.0
pymysql>=1.0  # optional, only if using MySQL
```

> Note: `xlrd` v2.0+ removed support for `.xlsx` files. If you need to read old `.xls` files, explicitly install `xlrd==1.2.0` or convert those files to `.xlsx` and use `openpyxl`.

---

## 🧾 database.sql (example)

```sql
-- Minimal example table for SQLite / MySQL
CREATE TABLE IF NOT EXISTS attainment_data (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  student VARCHAR(255),
  average_marks REAL,
  attainment_level VARCHAR(50),
  direct_attainment REAL,
  indirect_attainment REAL,
  final_attainment REAL,
  co_mapping TEXT,
  po_mapping TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

*(Adjust `AUTO_INCREMENT`/`SERIAL` as needed for your DB engine — e.g., use `INTEGER PRIMARY KEY AUTOINCREMENT` for SQLite.)*

---

## ♻️ Contributing

Contributions welcome — open an issue or create a PR. Suggested workflow:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes & push
4. Open a Pull Request

---

## 📝 License

This project is released under the **MIT License**. See `LICENSE` for details.

---

## 👨‍💻 Author

**Shrihari Kasar** — [GitHub](https://github.com/ShrihariKasar) — Computer Engineering Student
Portfolio: [https://shriharikasarportfolio.netlify.app/](https://shriharikasarportfolio.netlify.app/)

---

## 🖼️ Results Section (Figures)

Below are the screenshots of the NBA Attainment System.

<p align="center">
  <img src="static/home.png" alt="Home Page" width="600"><br>
  <b></b> This image shows the home page of the NBA Attainment System.
</p>

<p align="center">
  <img src="static/upload.png" alt="Upload Page" width="600"><br>
  <b></b> This image shows the file upload interface for academic data.
</p>

<p align="center">
  <img src="static/contact.png" alt="Contact Us Page" width="600"><br>
  <b></b> This image shows the "Contact Us" page with a contact form.
</p>

<p align="center">
  <img src="static/results_table.png" alt="Results Table" width="600"><br>
  <b></b> This image shows a table with student academic attainment results.
</p>

<p align="center">
  <img src="static/attainment_pie.png" alt="Attainment Pie Chart" width="600"><br>
  <b></b> This image shows a pie chart of the overall attainment distribution.
</p>

<p align="center">
  <img src="static/co_po_bar.png" alt="CO-PO Mapping Bar Graph" width="600"><br>
  <b></b> This image shows a bar graph of CO and PO mapping distribution.
</p>
