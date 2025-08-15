#Password Strength & Breach Checker

A simple Flask web app that:
- Checks the strength of a password.
- Checks if the password has been leaked in past breaches using HaveIBeenPwned API.
- Gives suggestions to make it stronger.

## Features
- Password strength meter (color-coded).
- Breach check via SHA-1 hashing (safe — password never sent directly).
- Mobile-friendly UI using Bootstrap.
- JSON API for programmatic use.

##Tech Stack
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Python Flask
- **API:** HaveIBeenPwned

## Installation
```bash
git clone <your-repo-url>
cd password_strength_checker
pip install -r requirements.txt
python app.py
```
Go to `http://127.0.0.1:5000` in your browser.


## 📜 License
MIT License
