# 🔐 CRITICAL: Setup GitHub Secrets

## ⚠️ THIS IS THE FINAL STEP TO ACTIVATE AUTOMATION!

Your code is now on GitHub, but the automation **won't work** until you add the email secrets.

---

## 📋 **Step-by-Step Instructions:**

### Step 1: Go to Your Repository Settings

**Click this link:** https://github.com/bhuviguru/Intern-Finder/settings/secrets/actions

*(Or manually navigate to: Repository → Settings → Secrets and variables → Actions)*

---

### Step 2: Add First Secret - SMTP_EMAIL

1. Click the **"New repository secret"** button
2. Fill in:
   - **Name:** `SMTP_EMAIL`
   - **Secret:** `bhuvanesh0709@gmail.com`
3. Click **"Add secret"**

---

### Step 3: Add Second Secret - SMTP_PASSWORD

1. Click **"New repository secret"** button again
2. Fill in:
   - **Name:** `SMTP_PASSWORD`
   - **Secret:** `drzuedahpdzxaoyx`
3. Click **"Add secret"**

---

## ✅ After Adding Secrets

You should see:
```
SMTP_EMAIL
SMTP_PASSWORD
```

Both will show as "Updated X seconds ago"

---

## 🧪 **Test the Automation (Optional but Recommended)**

1. Go to: https://github.com/bhuviguru/Intern-Finder/actions
2. Click on **"Daily Internship Bot"** workflow in the left sidebar
3. Click the **"Run workflow"** dropdown button (on the right)
4. Select branch: **main**
5. Click **"Run workflow"** button
6. Wait 2-5 minutes
7. **Check your email** for the internship report!

---

## 📅 **Automatic Schedule**

Once secrets are configured, the bot will run **automatically**:

- **Time:** Every day at **10:00 PM IST** (16:30 UTC)
- **Location:** GitHub's cloud servers (not your laptop!)
- **Email:** Sent to `bhuvanesh0709@gmail.com`
- **Content:** Top 15 internships + AI-generated answers

---

## 🎉 **YOU'RE DONE!**

After adding the secrets:
- ✅ Close your laptop
- ✅ Go to sleep
- ✅ The bot runs automatically every night
- ✅ Wake up to fresh internship opportunities in your inbox!

---

## ❓ **Troubleshooting**

**Q: I don't see the "New repository secret" button**
- A: Make sure you're logged into GitHub as the repository owner

**Q: The workflow runs but emails aren't sent**
- A: Double-check the secret names are exactly: `SMTP_EMAIL` and `SMTP_PASSWORD` (case-sensitive!)

**Q: How do I know it's working?**
- A: Check the Actions tab for green ✅ checkmarks, and check your email after 10 PM IST

---

**IMPORTANT LINKS:**
- Secrets Page: https://github.com/bhuviguru/Intern-Finder/settings/secrets/actions
- Actions Page: https://github.com/bhuviguru/Intern-Finder/actions
- Repository: https://github.com/bhuviguru/Intern-Finder
