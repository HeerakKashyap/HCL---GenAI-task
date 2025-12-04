# Installation Fix for Windows

## Issue
Numpy and other packages may try to build from source, requiring C/C++ compilers that aren't available on Windows.

## Solution

### Step 1: Upgrade pip, setuptools, and wheel
```bash
python -m pip install --upgrade pip setuptools wheel
```

### Step 2: Install packages one by one (if batch install fails)

Install numpy first (it's a dependency for other packages):
```bash
pip install numpy
```

Then install the rest:
```bash
pip install -r requirements.txt
```

### Alternative: Install packages individually

If you continue to have issues, install packages in this order:

```bash
pip install numpy
pip install flask flask-cors
pip install openai python-dotenv requests
pip install pdfplumber pypdf
pip install faiss-cpu
pip install sentence-transformers
```

### If faiss-cpu still fails

Try installing from conda-forge (if you have conda):
```bash
conda install -c conda-forge faiss-cpu
```

Or use the alternative approach - install faiss without version constraint:
```bash
pip install faiss-cpu --no-cache-dir
```

### Verify Installation

After installation, verify packages:
```bash
python -c "import numpy; import faiss; import flask; print('All packages installed successfully')"
```

