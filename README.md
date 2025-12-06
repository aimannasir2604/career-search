# Career Search - Career Guidance Platform

A comprehensive Flask-based web application for career guidance, personality assessment, and counselor booking.

## Features

- **Career Personality Quiz**: Interactive quiz to discover career paths based on personality traits
- **GPA Calculator**: Calculate and track academic performance
- **Counselor Booking**: Book appointments with multiple career counselors
- **Admin Panel**: Manage quiz questions and counselor profiles
- **User Profile**: Track quiz results, GPA, and appointments

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Modern gradient-based UI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aimannasir2604/career-search.git
cd career-search
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python app.py
```

6. Open browser and navigate to: `http://localhost:5000`

## Default Admin Credentials

- **Email**: admin202@gmail.com
- **Password**: admin202

## Deployment

### Option 1: Render (Recommended - Free Tier Available)

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: career-search
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Click "Create Web Service"

### Option 2: Railway

1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Flask and deploy
5. Your app will be live automatically

### Option 3: PythonAnywhere

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and sign up
2. Open Bash console
3. Clone your repo:
```bash
git clone https://github.com/aimannasir2604/career-search.git
```
4. Create virtual environment and install dependencies
5. Configure web app in Web tab
6. Set WSGI configuration file

### Option 4: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create career-search-app`
4. Deploy: `git push heroku main`
5. Open: `heroku open`

## Project Structure

```
career_search/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── runtime.txt           # Python version
├── templates/            # HTML templates
│   ├── home.html
│   ├── quiz.html
│   ├── consultation.html
│   └── ...
├── static/               # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── instance/            # Database files
```

## Environment Variables

For production, set:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key-here`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

