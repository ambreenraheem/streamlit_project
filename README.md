DATE: 05-FEBUARY-2026


# Building First Streamlit App
## By AMBREEN ABDUL RAHEEM
### (THE DATA ANALYST, AI AGENT AND WEB APPLICATION DEVELOPER)


Building a real-time web application using the Streamlit Python package.

The instructor demonstrates how to create an interactive dashboard that tracks bike and dock availability for Toronto’s Bike Share system by tapping into live API data.

Key features of the app include a color-coded map for station status and a personalized search function that calculates the shortest path to the nearest available bike or empty dock. Beyond technical coding steps involving folium and pandas, the tutorial emphasizes a product-driven mindset, encouraging viewers to focus on user experience and business impact in their data science projects.

The source ultimately highlights Streamlit as a no-cost, highly customizable alternative to traditional dashboarding tools like Tableau or Power BI.

### Important Note:

1️⃣ Windows-Compatible requirements.txt

A requirements.txt is a list of Python packages your project needs.

Example content:
```
numpy==1.26.4
pandas==2.2.2
streamlit==1.35.0
folium==0.16.0
```

Each line is either:

package → latest version

package==version → specific version

Windows-compatible means:

All packages listed can be installed on Windows without errors.

No macOS-only or Linux-only packages.

No OS-specific build strings (like py38h313beb8_8) that cause errors on Windows.

✅ Use case: You run:
```
pip install -r requirements.txt
```

and Windows installs all packages without failing.

2️⃣ Windows-Compatible environment.yml

An environment.yml is a Conda environment file.

It lists Python version, packages, and channels Conda uses.

Example:
```
name: bikeshare_streamlit
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pandas
  - numpy
  - matplotlib
  - scikit-learn
  - pip
  - pip:
      - streamlit
      - folium
      - geopandas
```

Windows-compatible means:

Only packages that can be installed on Windows

No macOS/Linux system libraries like libcxx or pyobjc

No OS-specific build strings (like osxarm64 or py38h123abc_0)

✅ Use case: You run:
```
conda env create -f environment.yml
conda activate bikeshare_streamlit
```

and Windows sets up a working Conda environment with all packages.
| Feature                 | requirements.txt      | environment.yml           |
|-------------------------|---------------------|--------------------------|
| Used by                 | pip                 | conda + pip              |
| Specifies OS builds?    | No                  | Can, if exported from another OS |
| Cross-platform friendly?| Usually yes (if pure Python) | Only if exported carefully |
| Python version included?| Optional            | Yes                      |
| Channels included?      | No                  | Yes (conda-forge, defaults) |


**💡 Rule of thumb:**

Use requirements.txt for pip-based installation.

Use environment.yml for full Conda environments, especially if you need scientific packages like numpy, pandas, or pyarrow.


### FOR MORE UPDATES FOLLOW ME:
### **YOUTUBE CHANNEL**
**[AMBREEN THE DATA ANALYST](https://www.youtube.com/@AmbreenAbdulRaheem-y8m)**

### **GitHub**
**[GitHub](https://github.com/ambreenraheem)**

### **LinkedIn**
**[LinkedIn](https://www.linkedin.com/in/ambreen-abdul-raheem-122509300/?locale=en)**
