#!/usr/bin/env python3
"""
GitHub Repository Setup Helper
Guides you through creating and linking your BIMMERAH repo on GitHub
"""

import subprocess
import webbrowser
import time

def run_cmd(cmd):
    """Run command silently"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

print("=" * 70)
print(" BIMMERAH: GitHub Repository Setup")
print("=" * 70)

print("\n📋 STEP 1: Create Repository on GitHub")
print("-" * 70)

print("""
Go to: https://github.com/new

Fill in:
  • Repository name: BIMMERAH
  • Description: Free Android version of BIMMERCODE app
  • Public or Private: Your choice
  
⚠️  DO NOT initialize with README, .gitignore, or license
    (Your code is already here!)

Then click "Create repository"
""")

print("\n📋 STEP 2: Link Local Repo to GitHub")
print("-" * 70)

print("""
After creating the repo on GitHub, copy the HTTPS or SSH URL.

Then run ONE of these commands:

HTTPS (Recommended - no SSH key needed):
  git remote add origin https://github.com/YOUR_USERNAME/BIMMERAH.git
  
SSH (Requires SSH key setup):
  git remote add origin git@github.com:YOUR_USERNAME/BIMMERAH.git

Replace YOUR_USERNAME with your actual GitHub username.
""")

print("\n📋 STEP 3: Push Your Code")
print("-" * 70)

print("""
After adding the remote, push your code:

  git push -u origin main

The -u flag sets up tracking for future pushes.
""")

print("\n" + "=" * 70)
print(" COMPLETE COPY-PASTE COMMAND SEQUENCE:")
print("=" * 70)

print("""
1. Create repo on https://github.com/new (BIMMERAH)

2. Copy this entire block and paste in PowerShell:

$username = Read-Host "Enter your GitHub username"
git remote add origin "https://github.com/$username/BIMMERAH.git"
git push -u origin main

3. When prompted, enter your GitHub credentials or personal token

""")

print("=" * 70)
print(" ✅ That's it!")
print("=" * 70)

print("""
Once pushed, go to: https://github.com/YOUR_USERNAME/BIMMERAH

The GitHub Actions workflow will:
  • Automatically build your APK
  • Create artifacts you can download
  • Complete in ~5-10 minutes
""")

input("\nPress Enter to continue...")
