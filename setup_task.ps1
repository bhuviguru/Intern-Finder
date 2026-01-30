$ErrorActionPreference = "Stop"

$TaskName = "InternshipBotDaily"
$ScriptPath = Join-Path $PSScriptRoot "run_finder.bat"

Write-Host "Setting up Advanced Windows Task..." -ForegroundColor Cyan

# Check if task exists and delete it
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Removed old task."
}

# Create Action
$Action = New-ScheduledTaskAction -Execute $ScriptPath

# Create Trigger (Daily at 10:00 PM)
$Trigger = New-ScheduledTaskTrigger -Daily -At "10:00PM"

# Create Settings
# - AllowStartIfOnBatteries: Run even if laptop is unplugged
# - DontStopIfGoingOnBatteries: Don't kill it if unplugged
# - StartWhenAvailable: Run ASAP if scheduled time was missed (System was off)
# - WakeToRun: Wake computer from sleep to run
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -WakeToRun `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Register Task
# -User "System" or current user? Current user is safer for paths, but requires password for "Run whether logged on or not"
# For simplicity with batch file run, we use current user interactive or "RunOnlyIfLoggedOn" if no password provided.
# However, "Run ASAP" usually works best with stored credentials.
# To avoid password prompt complexity in script, we'll use the interactive user context but set high privileges.

Register-ScheduledTask `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -TaskName $TaskName `
    -Description "Runs Internship Finder Bot Daily at 10 PM" `
    -RunLevel Highest

Write-Host "✅ Task '$TaskName' created successfully!" -ForegroundColor Green
Write-Host " - Runs Daily at 10:00 PM"
Write-Host " - Wakes computer from sleep"
Write-Host " - Runs ASAP if computer was off at 10:00 PM"
Write-Host "--------------------------------------------"
