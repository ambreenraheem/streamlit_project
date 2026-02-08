## This is Conda Environment for windows commands prompt,powershell, gitbash
#### 🔧 How to install properly on Windows

Inside your conda environment:
```
conda activate bikeshare_streamlit
pip install -r requirements.txt
```
⚠ Important Note

Because you're on Windows + Conda, it's better that numpy & pandas come from Conda first (fewer binary issues):
```
conda install numpy pandas pyarrow -y
pip install -r requirements.txt
```
🎯 Result

✔ No macOS libraries
✔ No system build pins
✔ Works on Windows
✔ Matches your project versions


Perfect — that’s exactly the correct sequence for Windows + Conda. ✅

Here’s why we do it this way:
```
conda install numpy pandas pyarrow -y
```
Conda provides precompiled binaries for these heavy packages.

Ensures Windows won’t fail compiling from source (common with NumPy, pandas, PyArrow).
```
pip install -r requirements.txt
```
Installs the remaining Python packages from your requirements.txt.

All pure Python packages (like Streamlit, Folium, Altair) work fine via pip.
```
# After this, test the environment:
conda activate bikeshare_streamlit
python -c "import numpy, pandas, pyarrow, streamlit, folium; print('All OK')"
```

If it prints All OK → everything is installed correctly.

Then you can run your app:
```
cd D:\streamlit_project
streamlit run bikeshare_app.py
```

### For GitHub

**Step 1 — Create a new repo on GitHub**

- Go to GitHub
- Click “New repository”
- Name it, for example: bikeshare_streamlit
- Do NOT initialize with README (we already have local files)
- Click Create repository

You will see instructions like:

```
git remote add origin https://github.com/yourusername/bikeshare_streamlit.git
git branch -M main
git push -u origin main
```
**Step 2 — Add remote to your local repo**

Run:
```
git remote add origin https://github.com/ambreenraheem/bikeshare_streamlit.git
```

Replace the URL with your GitHub repo URL.

**Step 3 — Set the main branch**

By default, your local branch is master. GitHub now prefers main. Rename your branch:
```
git branch -M main
```
**Step 4 — Commit your changes**

You already have staged files (git status shows them). Commit them:
```
git commit -m "Initial commit: add bikeshare app, environment, and requirements"
```
**Step 5 — Push to GitHub**
```
git push -u origin main
```

This will upload all files to GitHub.

The -u sets origin/main as default for future pushes.

**Step 6 — Verify**

Go to your GitHub repo page and refresh — you should see:

- bikeshare_app.py
- helpers.py
- environment.yml
- requirements.txt

All done ✅






