# Virtual Environment Setup Guide

## Why Use Virtual Environment?

Virtual environments isolate project dependencies, preventing conflicts with other Python projects and system packages.

## Setup Steps

### Windows

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
venv\Scripts\activate
```

3. Upgrade pip:
```bash
python -m pip install --upgrade pip
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Deactivate (when done):
```bash
deactivate
```

### Linux/Mac

1. Create virtual environment:
```bash
python3 -m venv venv
```

2. Activate virtual environment:
```bash
source venv/bin/activate
```

3. Upgrade pip:
```bash
python -m pip install --upgrade pip
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Deactivate (when done):
```bash
deactivate
```

## Running the Application

After activating the virtual environment:

1. Set up directories:
```bash
python setup.py
```

2. Start backend:
```bash
python app.py
```

3. In another terminal (activate venv first), start frontend:
```bash
cd client
npm install
npm start
```

## Important Notes

- Always activate the virtual environment before running Python scripts
- The virtual environment folder (`venv/`) is already in `.gitignore`
- If you see import errors, make sure the virtual environment is activated
- Install new packages only when the virtual environment is active

