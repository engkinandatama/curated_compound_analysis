# 🛠️ Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux Ubuntu 18.04+
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: Stable connection for API calls

### Recommended Requirements
- **Python**: 3.8 or higher
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **Browser**: Google Chrome (latest version)

## Step-by-Step Installation

### 1. Python Installation

#### Windows
```bash
# Download from python.org or use chocolatey
choco install python

# Verify installation
python --version
pip --version
```

#### macOS
```bash
# Using Homebrew
brew install python

# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/compound-analysis-pipeline.git
cd compound-analysis-pipeline
```

### 3. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv compound_env

# Activate virtual environment
# Windows
compound_env\Scripts\activate

# macOS/Linux
source compound_env/bin/activate
```

### 4. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# For development (optional)
pip install -r requirements-dev.txt
```

## ChromeDriver Setup

### Option 1: Automatic Installation (Recommended)

The script uses `webdriver-manager` to automatically download and manage ChromeDriver:

```python
# This happens automatically when you run the script
from webdriver_manager.chrome import ChromeDriverManager
```

### Option 2: Manual Installation

#### Step 1: Check Chrome Version
1. Open Google Chrome
2. Go to `chrome://version/`
3. Note the version number (e.g., `120.0.6099.109`)

#### Step 2: Download ChromeDriver
1. Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
2. Download the version that matches your Chrome version
3. For Chrome 115+, use [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)

#### Step 3: Extract and Place
```bash
# Windows
# Extract chromedriver.exe to project folder
unzip chromedriver_win32.zip
move chromedriver.exe /path/to/project/

# macOS
# Extract and make executable
unzip chromedriver_mac64.zip
chmod +x chromedriver
mv chromedriver /path/to/project/

# Linux
# Extract and make executable
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /path/to/project/
```

### Option 3: System PATH Installation

#### Windows
1. Extract ChromeDriver to a folder (e.g., `C:\chromedriver\`)
2. Add to System PATH:
   - Right-click "This PC" → Properties
   - Advanced System Settings → Environment Variables
   - Edit "Path" → Add `C:\chromedriver\`
3. Verify: `chromedriver --version`

#### macOS/Linux
```bash
# Move to system PATH
sudo mv chromedriver /usr/local/bin/

# Make executable
sudo chmod +x /usr/local/bin/chromedriver

# Verify
chromedriver --version
```

## Jupyter Notebook Setup

### 1. Install Jupyter
```bash
# Already included in requirements.txt
pip install jupyter notebook
```

### 2. Launch Jupyter
```bash
# Start Jupyter Notebook
jupyter notebook

# Or use JupyterLab
pip install jupyterlab
jupyter lab
```

### 3. Configure Kernel
```bash
# Add current environment to Jupyter
python -m ipykernel install --user --name=compound_env --display-name="Compound Analysis"
```

## Verification

### Test Installation
```bash
# Test Python imports
python -c "import pandas, selenium, requests; print('All imports successful!')"

# Test ChromeDriver
python -c "from selenium import webdriver; from webdriver_manager.chrome import ChromeDriverManager; print('ChromeDriver setup successful!')"
```

### Test Notebook
1. Open `notebooks/curated_compound_swiss_target.ipynb`
2. Run Cell 1 (Setup)
3. Check for any error messages

## Common Installation Issues

### Issue 1: Python Path Problems
```bash
# Windows: Use py launcher
py -m pip install -r requirements.txt

# macOS/Linux: Use python3 explicitly
python3 -m pip install -r requirements.txt
```

### Issue 2: Permission Errors
```bash
# Windows: Run as Administrator
# macOS/Linux: Use sudo or --user flag
pip install --user -r requirements.txt
```

### Issue 3: ChromeDriver Permission (macOS)
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine /path/to/chromedriver

# Or allow in System Preferences → Security & Privacy
```

### Issue 4: SSL Certificate Errors
```bash
# Upgrade pip and certificates
pip install --upgrade pip certifi

# Or use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Optional Enhancements

### 1. Git Configuration
```bash
# Set up git for contributions
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. IDE Setup
- **VS Code**: Install Python extension
- **PyCharm**: Configure Python interpreter
- **Jupyter**: Install extensions for better experience

### 3. Development Tools
```bash
# Install development dependencies
pip install pytest black flake8 mypy

# Pre-commit hooks
pip install pre-commit
pre-commit install
```

## Next Steps

After successful installation:
1. Review the [Usage Guide](usage.md)
2. Check the [Troubleshooting Guide](troubleshooting.md)
3. Try the sample data provided
4. Explore the example notebooks

## Support

If you encounter installation issues:
1. Check Python and pip versions
2. Verify internet connectivity
3. Review error messages carefully
4. Search existing issues on GitHub
5. Create a new issue with detailed error information
