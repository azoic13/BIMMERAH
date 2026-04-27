#!/usr/bin/env python3
"""
Interactive GitHub Setup Assistant
Guides you step-by-step through connecting to GitHub
"""

import subprocess
import sys
import webbrowser

def run_command(cmd):
    """Run a git command"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip(), result.stderr.strip()

def main():
    print("=" * 70)
    print(" BIMMERAH: GitHub Setup Assistant")
    print("=" * 70)
    
    # Check if remote already exists
    success, stdout, stderr = run_command("git remote -v")
    if stdout:
        print("\n⚠️  WARNING: Remote already configured:")
        print(stdout)
        response = input("\nRemove existing remote and reconfigure? (y/n): ")
        if response.lower() == 'y':
            run_command("git remote remove origin")
        else:
            print("Keeping existing remote.")
            return
    
    print("\n" + "=" * 70)
    print(" STEP 1: Create Repository on GitHub")
    print("=" * 70)
    
    print("""
We'll open GitHub to create your repository.

When creating:
  1. Name: BIMMERAH
  2. DO NOT initialize with README/.gitignore
  3. Click "Create repository"
""")
    
    open_github = input("\nOpen GitHub now? (y/n): ").lower()
    if open_github == 'y':
        webbrowser.open("https://github.com/new")
        print("✓ Opening https://github.com/new in your browser")
    
    print("""
⏸️  Pause here and:
  1. Create the BIMMERAH repository on GitHub
  2. Come back to this script
  3. Enter your username when prompted
""")
    
    input("\nPress Enter when repository is created...")
    
    print("\n" + "=" * 70)
    print(" STEP 2: Link Repository")
    print("=" * 70)
    
    username = input("\nEnter your GitHub username: ").strip()
    if not username:
        print("✗ Username required")
        sys.exit(1)
    
    url = f"https://github.com/{username}/BIMMERAH.git"
    print(f"\nConnecting to: {url}")
    
    success, stdout, stderr = run_command(f'git remote add origin "{url}"')
    if success:
        print("✓ Remote added successfully")
    else:
        print(f"✗ Failed to add remote: {stderr}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print(" STEP 3: Push Code to GitHub")
    print("=" * 70)
    
    print("""
Running: git push -u origin main

You'll be prompted for:
  • Username: Your GitHub username
  • Password: Your personal access token
    (NOT your GitHub password)

If you don't have a token:
  1. Go to: https://github.com/settings/tokens
  2. Click "Generate new token"
  3. Check "repo" scope
  4. Copy and paste it as password
""")
    
    input("\nPress Enter to push code...")
    
    success, stdout, stderr = run_command("git push -u origin main")
    
    if success or "up-to-date" in stdout.lower():
        print("\n✅ CODE PUSHED SUCCESSFULLY!")
        print(f"\nRepository: https://github.com/{username}/BIMMERAH")
    else:
        print(f"\n⚠️  Push output:")
        print(stdout)
        if stderr:
            print(f"Errors: {stderr}")
    
    print("\n" + "=" * 70)
    print(" STEP 4: Wait for GitHub Actions")
    print("=" * 70)
    
    print(f"""
Go to: https://github.com/{username}/BIMMERAH/actions

You should see "Build BIMMERAH APK" workflow running.

Wait for it to complete (~5-10 minutes), then:
  1. Click the completed workflow
  2. Scroll down to "Artifacts"
  3. Download "bimmerah-apk"
  4. Extract the ZIP file
  5. Place APK in: bin/bimmerah-0.1.0-debug.apk
""")
    
    input("\nPress Enter to open Actions page...")
    webbrowser.open(f"https://github.com/{username}/BIMMERAH/actions")
    
    print("\n" + "=" * 70)
    print(" ✅ SETUP COMPLETE!")
    print("=" * 70)
    
    print(f"""
Your repository is live at:
  https://github.com/{username}/BIMMERAH

Next steps:
  1. Download APK from GitHub Actions
  2. Run: adb install -r bin/bimmerah-0.1.0-debug.apk
  3. Launch: adb shell am start -n org.bimmerah.app/.MainActivity

Your Pixel 6 is ready! 🚀
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled")
        sys.exit(0)
