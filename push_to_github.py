#!/usr/bin/env python3
"""
Push Fixed Workflow to GitHub
Completes the setup and triggers the APK build
"""

import subprocess

print("=" * 70)
print(" BIMMERAH: Push Fixed Workflow to GitHub")
print("=" * 70)

print("\n✅ Fixed GitHub Actions workflow (deprecated versions updated)")
print("   • actions/checkout: v3 → v4")
print("   • actions/setup-java: v3 → v4")
print("   • actions/upload-artifact: v3 → v4")

print("\n" + "=" * 70)
print(" READY TO PUSH")
print("=" * 70)

print("""
Your code is committed and ready to push.

If you haven't set up GitHub yet:

1. Create repo at: https://github.com/new
   Name: BIMMERAH
   
2. Don't initialize with README/.gitignore

3. Run ONE of these:

   HTTPS (copy from GitHub after creating repo):
   git remote add origin https://github.com/YOUR_USERNAME/BIMMERAH.git
   
   Then push:
   git push -u origin main

4. GitHub Actions will automatically:
   • Start building APK (visible in Actions tab)
   • Complete in ~5-10 minutes
   • Create downloadable artifact
""")

print("\n" + "=" * 70)

# Check if remote is set up
result = subprocess.run(
    "git remote -v",
    shell=True,
    capture_output=True,
    text=True
)

if result.stdout:
    print(" ✓ REMOTE CONFIGURED")
    print("=" * 70)
    print(result.stdout)
    print("\nReady to push? (y/n): ", end="")
    if input().lower() == 'y':
        push_result = subprocess.run(
            "git push -u origin main",
            shell=True,
            capture_output=True,
            text=True
        )
        if push_result.returncode == 0:
            print("\n✅ Code pushed successfully!")
            print("\nGo to GitHub Actions to watch the build:")
            print("https://github.com/YOUR_USERNAME/BIMMERAH/actions")
        else:
            print(f"\nError: {push_result.stderr}")
else:
    print(" ⚠️  NO REMOTE CONFIGURED")
    print("=" * 70)
    print("""
You need to set up GitHub first.

Run: python github_setup_interactive.py

Or manually:
1. Create BIMMERAH repo on GitHub
2. Run: git remote add origin https://github.com/YOUR_USERNAME/BIMMERAH.git
3. Run: git push -u origin main
""")
