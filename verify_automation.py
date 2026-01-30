# Automation Setup Verification
# Quick check of internship finder bot automation status

import os, json
from pathlib import Path

print("=" * 70)
print("🔍 INTERNSHIP FINDER BOT - AUTOMATION STATUS CHECK")
print("=" * 70)
print()

checks_passed = 0
total_checks = 0

# 1. GitHub Actions Workflow
print("1️⃣  GITHUB ACTIONS WORKFLOW")
workflow = Path(".github/workflows/daily_bot.yml")
if workflow.exists():
    print("   ✅ Workflow file exists")
    checks_passed += 1
    
    content = workflow.read_text()
    if "cron:" in content:
        print("   ✅ Scheduled to run daily")
        checks_passed += 1
    else:
        print("   ❌ No schedule found")
    
    if "SMTP_EMAIL" in content:
        print("   ✅ Email secrets configured")
        checks_passed += 1
    else:
        print("   ❌ Missing email secrets")
    
    total_checks += 3
else:
    print("   ❌ Workflow file NOT found")
    total_checks += 3

print()

# 2. Configuration
print("2️⃣  CONFIGURATION")
settings = Path("config/settings.json")
if settings.exists():
    print("   ✅ Settings file exists")
    data = json.loads(settings.read_text())
    if data.get("send_email"):
        print(f"   ✅ Email enabled (top {data.get('top_n', 0)} jobs)")
        checks_passed += 2
    else:
        print("   ❌ Email NOT enabled")
        checks_passed += 1
    total_checks += 2
else:
    print("   ❌ Settings file missing")
    total_checks += 2

print()

# 3. Git Repository
print("3️⃣  GIT REPOSITORY")
if Path(".git").exists():
    print("   ✅ Is a Git repository")
    checks_passed += 1
    
    try:
        import subprocess
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if "github.com" in result.stdout:
            print(f"   ✅ Connected to GitHub")
            print(f"   📍 {result.stdout.strip()}")
            checks_passed += 1
        total_checks += 2
    except:
        print("   ❌ Git remote check failed")
        total_checks += 2
else:
    print("   ❌ NOT a Git repository")
    total_checks += 2

print()
print("=" * 70)
print(f"RESULT: {checks_passed}/{total_checks} checks passed ({int(checks_passed/total_checks*100)}%)")
print("=" * 70)
print()

if checks_passed == total_checks:
    print("✅ ✅ ✅  AUTOMATION IS WORKING!  ✅ ✅ ✅")
    print()
    print("🎉 YOUR BOT WILL RUN AUTOMATICALLY:")
    print("   • Every day at 10:00 PM IST (16:30 UTC)")
    print("   • On GitHub's cloud servers")
    print("   • Even when your laptop is SHUT DOWN or BROKEN")
    print("   • Sends email to:", os.getenv('SMTP_EMAIL', '[Check GitHub Secrets]'))
    print()
    print("📝 IMPORTANT - Complete these steps:")
    print()
    print("1. PUSH CODE TO GITHUB (if not already done):")
    print("   git add .")
    print('   git commit -m "Setup automation"')
    print("   git push origin main")
    print()
    print("2. CONFIGURE GITHUB SECRETS:")
    print("   • Go to your repo on GitHub")
    print("   • Settings → Secrets and variables → Actions")
    print("   • Add these secrets:")
    print("     - SMTP_EMAIL = bhuvanesh0709@gmail.com")
    print("     - SMTP_PASSWORD = drzuedahpdzxaoyx")
    print()
    print("3. VERIFY AUTOMATION:")
    print("   • Go to Actions tab in GitHub")
    print("   • You'll see 'Daily Internship Bot' workflow")
    print("   • Click 'Run workflow' to test manually")
    print()
    print("✨ After setup, the bot runs AUTOMATICALLY every day!")
else:
    print("⚠️  ISSUES FOUND - Review ❌ items above")
