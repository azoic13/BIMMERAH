#!/usr/bin/env python3
"""
GitHub Actions APK Build Setup Helper
Guides you through setting up cloud-based APK building
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a shell command and report status"""
    try:
        print(f"\n[*] {description}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description}")
            if result.stdout:
                print(result.stdout.strip())
            return True
        else:
            print(f"✗ {description}")
            if result.stderr:
                print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 70)
    print(" BIMMERAH: GitHub Actions Cloud APK Build Setup")
    print("=" * 70)
    
    print("\n📋 WHAT THIS DOES:")
    print("  • Automatically builds APK in cloud (GitHub Actions)")
    print("  • No local Android SDK/Java setup needed")
    print("  • Uses Python 3.11 (compatible with buildozer)")
    print("  • Creates artifacts you can download")
    
    print("\n🚀 QUICK START:")
    print("\n1. Push your code to GitHub:")
    print("   git add .")
    print("   git commit -m 'Initial BIMMERAH release'")
    print("   git push origin main")
    
    print("\n2. Go to your GitHub repo → Actions tab")
    print("   The 'Build BIMMERAH APK' workflow will start automatically")
    
    print("\n3. Download the APK:")
    print("   • Wait for workflow to complete (~5-10 minutes)")
    print("   • Go to the workflow run")
    print("   • Download 'bimmerah-apk' artifact")
    print("   • APK will be: bimmerah-0.1.0-debug.apk")
    
    print("\n4. Install on your device:")
    print("   adb install -r path/to/bimmerah-0.1.0-debug.apk")
    print("   adb shell am start -n org.bimmerah.app/.MainActivity")
    
    print("\n📝 CURRENT SETUP STATUS:")
    
    # Check git
    if run_command("git --version", "Git installed"):
        # Check if we're in a git repo
        if os.path.exists(".git"):
            print("✓ Git repository initialized")
        else:
            print("⚠ Not a git repository. Initialize with:")
            print("   git init")
            print("   git remote add origin https://github.com/YOUR_USERNAME/BIMMERAH.git")
    
    # Check GitHub Actions workflow
    workflow_file = ".github/workflows/build-apk.yml"
    if os.path.exists(workflow_file):
        print(f"✓ GitHub Actions workflow configured: {workflow_file}")
    else:
        print(f"⚠ Workflow not found: {workflow_file}")
    
    # Check buildozer.spec
    if os.path.exists("buildozer.spec"):
        print("✓ buildozer.spec configured")
    else:
        print("⚠ buildozer.spec not found")
    
    # Check requirements.txt
    if os.path.exists("requirements.txt"):
        print("✓ requirements.txt present")
    else:
        print("⚠ requirements.txt not found")
    
    print("\n" + "=" * 70)
    print(" ALTERNATIVE: Manual Cloud Build Services")
    print("=" * 70)
    
    print("\nIf you don't use GitHub:")
    
    print("\n1. EAS Build (Expo)")
    print("   • Website: https://eas.expo.dev")
    print("   • Setup: npm install -g eas-cli")
    print("   • Build: eas build --platform android")
    
    print("\n2. BeeJee")
    print("   • Website: https://beejee.io")
    print("   • Drag & drop your project")
    print("   • Download APK")
    
    print("\n3. AppVeyor")
    print("   • Website: https://www.appveyor.com")
    print("   • Configure appveyor.yml")
    print("   • Automated Android builds")
    
    print("\n" + "=" * 70)
    print("\n✅ Next Steps:")
    print("   1. Push to GitHub (if using GitHub Actions)")
    print("   2. Download APK artifact")
    print("   3. Run: adb install -r <apk-file>")
    print("   4. Enjoy BIMMERAH on your Pixel 6! 🚀")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
