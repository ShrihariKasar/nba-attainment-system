# 🎓 NBA Attainment System

A **web-based NBA Attainment Calculation System** built using **Flask, MySQL, and Bootstrap**.  
This system helps faculty, staff, and students manage and analyze **attainment levels** for courses as per **NBA (National Board of Accreditation) standards**.

---

## 🚀 Features

- **User Roles**
  - **Admin:** Manage users, approve submissions, and generate reports.
  - **Staff:** Upload attendance, study materials, notices, and attainment data.
  - **Students:** Submit projects, view attendance, achievements, and notices.

- **NBA Attainment Calculation**
  - Direct and indirect attainment levels
  - Final attainment percentage auto-calculated
  - High/Medium/Low classification with color coding

- **Data Management**
  - Project submissions with admin approval
  - Achievements & event management
  - Study materials & announcements upload/view
  - Attendance upload (Excel) and student view popup

- **Visualization**
  - Dynamic tables with color-coded attainment levels
  - Scrollable popups for attendance
  - Clean Bootstrap-based UI with responsive design

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Other:** Font Awesome, jQuery

---

## 📂 Project Structure

nba-attainment-system/
│── app.py # Main Flask app
│── requirements.txt # Python dependencies
│── templates/ # HTML templates
│ ├── base.html
│ ├── dashboard.html
│ ├── attainment.html
│ └── ...
│── static/ # CSS, JS, Images
│ ├── css/
│ ├── js/
│ └── uploads/
│── database.sql # MySQL schema & tables
│── README.md # Project Documentation

yaml
Copy code

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShrihariKasar/nba-attainment-system.git
   cd nba-attainment-system
Create a virtual environment & install dependencies

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
Setup MySQL database

sql
Copy code
CREATE DATABASE nba_system;
USE nba_system;
SOURCE database.sql;
Run the Flask server

bash
Copy code
flask run
Access the app in browser

cpp
Copy code
http://127.0.0.1:5000
📊 Sample NBA Attainment Table
Student	Avg Marks	Attainment Level	Direct (%)	Indirect (%)	Final (%)
John D.	78	High	75	80	77.5
Mary K.	62	Medium	60	65	62.5
Rahul P.	45	Low	40	50	45.0

✅ Attainment levels are color-coded (Green = High, Yellow = Medium, Red = Low).

🏆 Future Scope
Integration with Excel/PDF export for attainment reports

Role-based email/SMS notifications

Automated CO-PO mapping and report generation

AI-based insights for weak students’ performance

🤝 Contributing
Contributions are welcome! Please fork this repository and submit a pull request.

📜 License
This project is licensed under the MIT License – feel free to use and modify for educational purposes.

👨‍💻 Author
Developed by Shrihari Kasar
(Computer Department Student)