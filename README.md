# Online Voting System

A secure, modern, and transparent web-based voting platform built using the Django framework, PostgreSQL, and styled with a premium glassmorphic UI.

---

## 🌟 Key Features

*   **Secure Email OTP Registration:** A two-step registration flow that sends a 6-digit verification code to the user's email to verify their identity before account creation.
*   **Frosted Glass UI (Glassmorphism):** High-end visual panels with dynamic mouse-tracking spotlight reflections and smooth micro-animations.
*   **Voter Dashboard:** A central panel featuring live account statistics (type, verification status, system online check) and clear action directions.
*   **Live Election Results:** Transparent visual graphs showing current vote counts and standings in real-time.
*   **Robust Admin Panel:** A built-in management console where administrators can manage users, add voting positions, and register candidates with profile pictures.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.11+, Django 5.x
*   **Database:** PostgreSQL 15+ (can also fall back to SQLite)
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5, FontAwesome Icons
*   **Email Dispatch:** Django SMTP / Console Backends

---

## 🚀 Getting Started (Setup & Execution Guide)

Follow these systematic steps to run this project locally on your machine:

### 1. Clone the project and navigate to the directory
Open your command terminal (Command Prompt or PowerShell) and enter:
```powershell
cd OnlineVotingSystem
```

### 2. Set up the virtual environment
Create a fresh, isolated Python environment to manage dependencies:
```powershell
python -m venv .venv
```

### 3. Activate the virtual environment
*   **PowerShell:**
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
*   **Command Prompt (CMD):**
    ```cmd
    .\.venv\Scripts\activate.bat
    ```
*(Once active, you will see `(.venv)` displayed at the start of your command prompt).*

### 4. Install dependencies
Install all required libraries listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 5. Configure the Database
By default, the project expects a local PostgreSQL server.
1. Make sure you have **PostgreSQL** running on your computer.
2. Create a local database named **`onlinevotingsystem`**.
3. Open `onlineVotingSystem/settings.py` and ensure the database credentials match your local setup:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'onlinevotingsystem',
           'USER': 'postgres',
           'PASSWORD': 'YOUR_PASSWORD_HERE',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### 6. Create database tables (Migrations)
Sync Django's code models to your PostgreSQL database:
```powershell
python manage.py migrate
```

### 7. Create an Administrator account
Generate your master login credentials for the backend panel:
```powershell
python manage.py createsuperuser
```
*(Follow the prompts to enter a username, email, and password).*

### 8. Run the development server
Start the web server:
```powershell
python manage.py runserver
```

---

## 📧 Email Configuration (OTP Flow)

Open `onlineVotingSystem/settings.py` to configure how registration verification codes are sent:

### Option A: Print OTP to Console (For Development)
The application will print the 6-digit verification code directly inside your running PyCharm terminal for easy copying:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Option B: Send to Real Gmail Inbox (For Production)
The system will send the OTP code to the registering user's actual inbox:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  
EMAIL_HOST_PASSWORD = 'your-16-character-google-app-password'  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```
*(Note: You must generate a **Google App Password** from your Google Account settings to populate `EMAIL_HOST_PASSWORD`)*.

---

## 📁 Project Structure

*   `onlineVotingSystem/` - Project configuration settings, routing, and WSGI entry points.
*   `poll/` - Application logic including views, database models, and forms.
*   `poll/templates/` - HTML files governing layout, dashboard, register, login, and candidate lists.
*   `poll/static/` - Custom CSS files (`style.css`) and generated neon banner illustration assets.
*   `media/` - Holds user-uploaded files, such as candidate profile photos.
*   `requirements.txt` - Lists all libraries required to run this app.
