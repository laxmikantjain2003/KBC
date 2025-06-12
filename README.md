 🎮 KBC - Kaun Banega Crorepati (Flask Based Game)

Welcome to the Python + Flask-based *KBC (Kaun Banega Crorepati)* game project! This is a quiz game inspired by the famous TV show, featuring lifelines, timer, login/registration system, and a leaderboard.

🧠 Features

- ✅ User Registration & Login
- 🎯 15 Questions with Increasing Difficulty
- 🧭 Lifelines:
  - 50-50
  - Phone-a-Friend
  - Audience Poll
  - Skip
- ⏲ Timer system for each question
- 🧾 Scorecard & Feedback
- 🏆 Leaderboard (Top 5 Players)
- 🖼 Beautiful UI with CSS, Bootstrap & Logo
- 🔒 SQLite Database Integration
- 
- ## 📁 Project Structure
- **KBC**
- __pychache__
- app.py
- question.json
- database = kbc.db
- Statics = Script.js, style.css, logo.png
- template = game.html, leaderboard.html, login.html, play.html, register.html, scorecard.html, splash.html
  
## 🚀 How to Run
### 1. Clone this repository
```bash
git clone https://github.com/laxmikantjain2003/KBC.git
cd KBC

2. Install Dependencies
Make sure Python 3 is installed. Then run:
pip install flask

3. Create the Database
python create_db.py

4. Start the Flask App
python app.py

Visit http://127.0.0.1:5000/ in your browser.

🧪 Testing
Register a new player.
Login and start the game.
Use all lifelines.
Let the timer run out.
Check leaderboard after the game.

👨‍💻 Technologies Used
Python
Flask
SQLite
HTML/CSS
JavaScript
Bootstrap

Made by [Laxmikant Jain](https://github.com/laxmikantjain2003)
