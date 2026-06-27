# How to push this package to GitHub

Because the ChatGPT GitHub connector may be read-only/restricted-write in some sessions, push from local PowerShell.

## 1. Unzip package

Unzip `DNB_REAL_V1_ENGINEERING_PACKAGE.zip` to:

```text
D:\DNB_REAL_V1_ENGINEERING_PACKAGE
```

## 2. Initialize Git

```powershell
cd D:\DNB_REAL_V1_ENGINEERING_PACKAGE

git init

git branch -M main
```

## 3. Connect to existing GitHub repo

For your repo:

```text
https://github.com/BOLI-LEO/myself
```

Run:

```powershell
git remote add origin https://github.com/BOLI-LEO/myself.git
```

If remote already exists:

```powershell
git remote set-url origin https://github.com/BOLI-LEO/myself.git
```

## 4. Commit and push

```powershell
git add .

git commit -m "init DNB-Reverse REAL-V1 engineering package"

git push -u origin main
```

## 5. If push is rejected because remote has existing files

Use:

```powershell
git pull origin main --allow-unrelated-histories

git push -u origin main
```

If the remote only contains old zip files and you want this project to replace it, create a new empty GitHub repo or manually clean old files first.
