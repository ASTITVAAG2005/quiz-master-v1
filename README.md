# Quiz Master

> A comprehensive quiz management system for educational institutions, enabling seamless quiz creation, participation, and performance tracking for both administrators and students.

---

## 🚀 Features

- **User Authentication:** Secure login for students and administrators
- **Quiz Management:** Create, edit, and delete quizzes with multiple question types
- **Real-Time Participation:** Students can attempt quizzes and view instant results
- **Performance Analytics:** Visual dashboards for user and quiz statistics
- **Admin Dashboard:** Monitor user activity, quiz attempts, and overall platform usage
- **Responsive UI:** Modern, user-friendly interface for all devices

---

## 🖥️ System Overview

Quiz Master is a web-based platform designed to simplify quiz management for educational institutions. It supports:

- **Admin Role:** Create, update, and delete quizzes, manage users, and view analytics.
- **Student Role:** Attempt quizzes, view scores, and track personal performance.

The system ensures secure access, real-time feedback, and insightful analytics for both users and administrators.

---

## 👤 User Roles & Functionalities

### Administrator
- Add, edit, and delete quizzes and questions
- View all users and their quiz attempts
- Analyze quiz statistics and user participation

### Student
- Register and log in securely
- Attempt available quizzes
- View quiz scores and performance history

---

## 🏗️ Project Structure

- `app.py` — Main application file (Flask backend)
- `mydatabase.sqlite3` — SQLite database for persistent storage
- `static/` — Static assets (images, CSS, JS)
- `templates/` — HTML templates (Jinja2)

---

## 🛠️ Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap, JavaScript (Jinja2 templating)
- **Database:** SQLite3
- **Visualization:** Matplotlib (for admin statistics)

---

## 📦 Getting Started

1. **Clone the repository:**
	```sh
	git clone https://github.com/ASTITVAAG2005/quiz-master-v1.git
	cd quiz-master-v1
	```
2. **Install dependencies:**
	```sh
	pip install -r requirements.txt
	```
3. **Run the application:**
	```sh
	python app.py
	```
4. **Access the app:**
	Open your browser and go to `http://localhost:5000`

---

## 🗄️ Database Schema (Overview)

- **users**: Stores user credentials and roles (admin/student)
- **quizzes**: Quiz metadata (title, description, etc.)
- **questions**: Questions linked to quizzes
- **options**: Multiple-choice options for questions
- **attempts**: Records of user quiz attempts and scores

---

## 📸 Screenshots

<div align="center">
<img src="static/admin_dashboard.html" alt="Admin Dashboard" width="400"/>
<img src="static/user_dashboard.html" alt="User Dashboard" width="400"/>
</div>

---

## 💡 Usage

1. **Admin Login:** Use admin credentials to access the dashboard and manage quizzes.
2. **Student Registration:** New users can register and log in to attempt quizzes.
3. **Quiz Attempt:** Students select a quiz, answer questions, and submit for instant scoring.
4. **View Results:** Both students and admins can view detailed performance analytics.

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

<div align="center">

### **Astitva Agarwal**
*Data Science & Artificial Intelligence Student*  
*Indian Institute of Technology Madras*

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/ASTITVAAG2005)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/astitva-agarwal-b587422a6)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:astitvaag2005@gmail.com)

</div>

---

## 📚 Project Context

This project was developed as part of the curriculum at **IIT Madras** with a focus on:

- **Quiz Automation:** Streamlining quiz management for educators and students
- **Data Visualization:** Providing actionable insights through analytics
- **Full-stack Development:** End-to-end solution using Python (Flask), SQLite, HTML, CSS, and JS

---

⭐ **Star this repository if you found it helpful!** ⭐

