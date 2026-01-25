# Internship Finder Bot - User Guide

## 🚀 Easy Setup (For New Users)

### 1. Requirements
- Download & Install [Python](https://www.python.org/downloads/) (Make sure "Add Python to PATH" is checked during installation)

### 2. Installation
1. Download/Unzip this folder.
2. Double-click `setup_daily_automation.bat` (Run as Administrator).
   - This will automatically:
     - Install required libraries.
     - Install browser drivers.
     - Create a `.env` file if it's missing.
     - Schedule the bot to run daily at 9:00 AM.

### 3. Configuration
1. Open `.env` file with Notepad.
2. Enter your email credentials:
   ```
   SMTP_EMAIL=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```
   *(Note: For Gmail, use an App Password, not your login password)*

3. (Optional) Customize search in `config/companies.json` or `config/keywords.json`.

---

## 📅 Daily Automation
Once you run the setup script, the bot is set to 9:00 AM daily.
- You can restart your PC; the task remembers.
- You don't need to keep any window open.

## 🧪 Testing
To test immediately:
Run command prompt in the folder and type:
```bash
python -m src.main
```

## ❓ Troubleshooting
- **No Email?** Check `.env` password and "Spam" folder.
- **Errors?** Check `logs/bot.log`.
