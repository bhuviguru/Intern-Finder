# 🤖 Internship Finder Bot - The Ultimate Guide

Welcome to your automated internship hunter! This bot works for you 24/7.

## 📥 How to Install (For New Users)
1.  **Download Code**: Clone this repo or unzip the folder.
2.  **Secret Key**: Create a file named `.env` in the folder and add:
    ```ini
    SMTP_EMAIL=your_email@gmail.com
    SMTP_PASSWORD=your_app_password
    DB_NAME=internships.db
    ```
    *(Need an App Password? Go to Google Account > Security > 2-Step Verification > App Passwords)*

3.  **One-Click Setup**:
    *   Right-click `setup_daily_automation.bat`
    *   Select **Run as Administrator**
    *   Done! 🟢

---

## 📅 Automatic Schedule
The bot is now programmed to run **Daily at 9:00 AM**.

### "What if my laptop is OFF?" 🛑
*   **Don't worry.** The automation is "Self-Healing".
*   If your laptop is off at 9:00 AM, the bot will run **immediately** the moment you turn it on.
*   It logs every run in `logs/task_output.log` so you can verify it.

---

## ☁️ Cloud Mode (Optional)
If you want it to run even when your laptop is broken/lost:
1.  Go to your GitHub Repository Settings.
2.  Add Secrets: `SMTP_EMAIL` and `SMTP_PASSWORD`.
3.  GitHub's servers will now run it for you every day.

---

## ❓ FAQ
*   **How do I stop it?**
    *   Open `Task Scheduler` app -> Right-click `InternshipBotDaily` -> Disable.
*   **Where are the internships?**
    *   Check your email! 📧  (And `internships.db` file for history).
*   **Is my password safe?**
    *   Yes. It stays on your laptop in the `.env` file. It is never shared.

Enjoy your automated career growth! 🚀
