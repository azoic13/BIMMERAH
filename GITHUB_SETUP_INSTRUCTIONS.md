# 🚀 BIMMERAH GitHub Setup - Final Steps

## Status ✅
Your local git repository is ready with all code committed:
```
Branch: main
Commits: Ready to push
Files: All tracked
```

---

## Step 1️⃣: Create GitHub Repository

Go to: **https://github.com/new**

Fill in the form:
- **Repository name**: `BIMMERAH`
- **Description**: `Free Android version of BIMMERCODE app`
- **Visibility**: Public (or Private if you prefer)
- ⚠️ **IMPORTANT**: Leave unchecked:
  - ☐ Add a README file
  - ☐ Add .gitignore
  - ☐ Choose a license

Click **"Create repository"**

---

## Step 2️⃣: Add GitHub Remote

After creating the repo, GitHub will show you a page with instructions.

**Copy your HTTPS URL** (looks like):
```
https://github.com/YOUR_USERNAME/BIMMERAH.git
```

Run in PowerShell:
```powershell
cd C:\Projects\BIMMERAH

git remote add origin https://github.com/YOUR_USERNAME/BIMMERAH.git
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

---

## Step 3️⃣: Push to GitHub

```powershell
git push -u origin main
```

You'll be prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Your GitHub personal access token (not your password)

If you don't have a token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`
4. Copy and paste it as the password

---

## Step 4️⃣: Watch GitHub Actions Build

Once pushed:
1. Go to: `https://github.com/YOUR_USERNAME/BIMMERAH`
2. Click the **Actions** tab
3. You'll see "Build BIMMERAH APK" workflow running
4. Wait for it to complete (~5-10 minutes)
5. Download the **bimmerah-apk** artifact

---

## Step 5️⃣: Install on Device

Once you have the APK from GitHub Actions:

```powershell
cd C:\Projects\BIMMERAH

# Extract the artifact ZIP and place APK in bin/

adb install -r bin/bimmerah-0.1.0-debug.apk

adb shell am start -n org.bimmerah.app/.MainActivity
```

---

## 🎯 Quick Copy-Paste

Paste this entire block in PowerShell (one at a time):

```powershell
# 1. Set your GitHub username
$username = Read-Host "Enter your GitHub username"

# 2. Add remote
git remote add origin "https://github.com/$username/BIMMERAH.git"

# 3. Push code
git push -u origin main
```

Then follow GitHub authentication prompts.

---

## ✅ You're All Set!

Once the APK is ready:
- Download from GitHub Actions
- Run: `adb install -r bin/bimmerah-0.1.0-debug.apk`
- Launch: `adb shell am start -n org.bimmerah.app/.MainActivity`
- Check logs: `adb logcat | grep -i bimmerah`

Your Pixel 6 is waiting! 🚀
