# Deployment Guide - Career Search

## 🚀 Quick Deployment Options

### 1. Render.com (Easiest - Free Tier)

**Steps:**

1. **Sign up** at [render.com](https://render.com) (use GitHub account)

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `aimannasir2604/career-search`
   - Click "Connect"

3. **Configure Settings:**
   - **Name**: `career-search` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free (or paid if you want)

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://career-search.onrender.com`

**Note:** Free tier apps sleep after 15 minutes of inactivity.

---

### 2. Railway.app (Recommended - Free Tier)

**Steps:**

1. **Sign up** at [railway.app](https://railway.app) (use GitHub account)

2. **Create Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `aimannasir2604/career-search`

3. **Auto-Deploy:**
   - Railway auto-detects Flask
   - Automatically installs dependencies
   - Your app will be live in 2-3 minutes

4. **Get URL:**
   - Railway provides a URL like: `https://career-search-production.up.railway.app`

**Advantages:**
- ✅ Auto-deploys on every git push
- ✅ Free $5 credit monthly
- ✅ No sleep (unlike Render free tier)

---

### 3. PythonAnywhere (Good for Beginners)

**Steps:**

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Open Bash Console** (from dashboard)

3. **Clone Repository:**
```bash
cd ~
git clone https://github.com/aimannasir2604/career-search.git
cd career-search
```

4. **Setup Virtual Environment:**
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configure Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask" → Python 3.10
   - Set source code: `/home/yourusername/career-search`
   - Set WSGI file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

6. **Edit WSGI File:**
```python
import sys
path = '/home/yourusername/career-search'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

7. **Reload Web App** (click reload button)

**Free tier:** `yourusername.pythonanywhere.com`

---

### 4. Heroku (Paid/Requires Credit Card)

**Steps:**

1. **Install Heroku CLI:**
   - Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login:**
```bash
heroku login
```

3. **Create App:**
```bash
heroku create career-search-app
```

4. **Deploy:**
```bash
git push heroku main
```

5. **Open:**
```bash
heroku open
```

**Note:** Heroku free tier is discontinued. Requires paid plan.

---

## 📋 Pre-Deployment Checklist

- [x] ✅ All code committed to GitHub
- [x] ✅ `requirements.txt` is up to date
- [x] ✅ `Procfile` created
- [x] ✅ `runtime.txt` created (for Heroku)
- [x] ✅ Database will be created automatically on first run
- [x] ✅ Admin credentials are set in code

## 🔧 Important Notes

1. **Database:** SQLite database will be created automatically on first deployment
2. **Admin Login:** 
   - Email: `admin202@gmail.com`
   - Password: `admin202`
3. **Environment Variables:** Set `FLASK_ENV=production` for production
4. **Secret Key:** Consider changing `app.secret_key` in `app.py` for production

## 🌐 After Deployment

1. Visit your live URL
2. Test all features:
   - Quiz functionality
   - Booking system
   - Admin panel
3. Share the URL with users!

## 📞 Need Help?

If you face any issues during deployment, check:
- Platform-specific logs
- Error messages in deployment console
- GitHub repository is public (for free tiers)

---

**Recommended:** Start with **Railway** or **Render** - they're the easiest!

