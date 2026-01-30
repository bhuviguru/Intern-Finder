"""
Automation Setup Verification Script
Checks if the internship finder bot is properly configured for cloud automation
"""

import os
import json
from pathlib import Path

def check_mark(passed):
    return "✅" if passed else "❌"

def main():
    print("=" * 70)
    print("🔍 INTERNSHIP FINDER BOT - AUTOMATION VERIFICATION")
    print("=" * 70)
    print()
    
    all_checks = []
    
    # 1. Check GitHub Actions Workflow File
    print("1️⃣  GITHUB ACTIONS WORKFLOW")
    workflow_file = Path(".github/workflows/daily_bot.yml")
    workflow_exists = workflow_file.exists()
    print(f"   {check_mark(workflow_exists)} Workflow file exists: {workflow_file}")
    all_checks.append(workflow_exists)
    
    if workflow_exists:
        with open(workflow_file, 'r') as f:
            content = f.read()
            has_schedule = 'schedule:' in content and 'cron:' in content
            has_manual_trigger = 'workflow_dispatch' in content
            has_secrets = 'SMTP_EMAIL' in content and 'SMTP_PASSWORD' in content
            
            print(f"   {check_mark(has_schedule)} Scheduled to run daily (cron job)")
            print(f"   {check_mark(has_manual_trigger)} Manual trigger enabled")
            print(f"   {check_mark(has_secrets)} Using GitHub Secrets for credentials")
            all_checks.extend([has_schedule, has_manual_trigger, has_secrets])
    
    print()
    
    # 2. Check Configuration Files
    print("2️⃣  CONFIGURATION FILES")
    
    # Settings.json
    settings_file = Path("config/settings.json")
    settings_exists = settings_file.exists()
    print(f"   {check_mark(settings_exists)} Settings file exists")
    all_checks.append(settings_exists)
    
    if settings_exists:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            email_enabled = settings.get('send_email', False)
            print(f"   {check_mark(email_enabled)} Email notifications enabled")
            print(f"   📧 Will send top {settings.get('top_n', 0)} matches")
            all_checks.append(email_enabled)
    
    # Keywords.json
    keywords_file = Path("config/keywords.json")
    keywords_exists = keywords_file.exists()
    print(f"   {check_mark(keywords_exists)} Keywords file exists")
    all_checks.append(keywords_exists)
    
    print()
    
    # 3. Check Required Files
    print("3️⃣  REQUIRED PROJECT FILES")
    required_files = [
        "src/main.py",
        "requirements.txt",
        "internships.db"
    ]
    
    for file_path in required_files:
        exists = Path(file_path).exists()
        print(f"   {check_mark(exists)} {file_path}")
        all_checks.append(exists)
    
    print()
    
    # 4. Check Git Repository
    print("4️⃣  GIT REPOSITORY")
    git_dir = Path(".git")
    is_git_repo = git_dir.exists()
    print(f"   {check_mark(is_git_repo)} Is a Git repository")
    all_checks.append(is_git_repo)
    
    if is_git_repo:
        # Check if remote is configured
        try:
            import subprocess
            result = subprocess.run(['git', 'remote', '-v'], 
                                  capture_output=True, text=True, check=True)
            has_remote = 'github.com' in result.stdout
            print(f"   {check_mark(has_remote)} Connected to GitHub repository")
            if has_remote:
                # Extract repo URL
                for line in result.stdout.split('\n'):
                    if 'origin' in line and '(push)' in line:
                        url = line.split()[1]
                        print(f"   📍 Repository: {url}")
                        break
            all_checks.append(has_remote)
        except Exception as e:
            print(f"   ❌ Error checking git remote: {e}")
            all_checks.append(False)
    
    print()
    
    # 5. Environment Variables Check
    print("5️⃣  ENVIRONMENT VARIABLES (.env)")
    env_file = Path(".env")
    env_exists = env_file.exists()
    print(f"   {check_mark(env_exists)} .env file exists (local only)")
    
    if env_exists:
        from dotenv import load_dotenv
        load_dotenv()
        
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        has_email = bool(smtp_email)
        has_password = bool(smtp_password)
        
        print(f"   {check_mark(has_email)} SMTP_EMAIL configured: {smtp_email if has_email else 'NOT SET'}")
        print(f"   {check_mark(has_password)} SMTP_PASSWORD configured: {'***' if has_password else 'NOT SET'}")
        
        print(f"   ⚠️  Note: .env is for local testing only")
        print(f"   ⚠️  GitHub Actions uses GitHub Secrets (not .env)")
    
    print()
    
    # Summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Checks Passed: {passed}/{total} ({percentage:.0f}%)")
    print()
    
    if percentage == 100:
        print("✅ ✅ ✅  ALL CHECKS PASSED!  ✅ ✅ ✅")
        print()
        print("🎉 Your bot is READY for cloud automation!")
        print()
        print("NEXT STEPS:")
        print("1. Make sure you've pushed the code to GitHub:")
        print("   git add .")
        print("   git commit -m 'Setup automated workflow'")
        print("   git push origin main")
        print()
        print("2. Configure GitHub Secrets:")
        print("   Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions")
        print("   Add these secrets:")
        print("   - SMTP_EMAIL: Your Gmail address")
        print("   - SMTP_PASSWORD: Your Gmail app password")
        print()
        print("3. The bot will run automatically EVERY DAY at 10:00 PM IST")
        print("   (Even when your laptop is OFF or BROKEN!)")
        print()
        print("4. You can also trigger it manually from GitHub Actions tab")
        print()
    elif percentage >= 70:
        print("⚠️  MOST CHECKS PASSED - Minor issues to fix")
        print()
        print("Please review the ❌ items above and fix them.")
    else:
        print("❌ CRITICAL ISSUES FOUND")
        print()
        print("Please fix the ❌ items above before the bot can work automatically.")
    
    print("=" * 70)
    
    return percentage == 100

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error running verification: {e}")
        exit(1)
