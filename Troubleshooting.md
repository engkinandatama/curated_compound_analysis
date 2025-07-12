# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### PubChem API Issues

#### Issue: Low Success Rate (< 50%)
**Symptoms:**
- Many compounds returning "Failed" status
- Timeout errors in logs
- Empty CID/SMILES results

**Solutions:**
1. **Check Compound Names**
   ```python
   # Verify compound names are correct
   common_issues = [
       "Typos in names",
       "Non-standard naming",
       "Brand names vs generic names",
       "Special characters"
   ]
   
   # Manual verification
   print("Checking compound names:")
   for name in df_input['Name'].head(10):
       print(f"- '{name}' (Length: {len(name)})")
   ```

2. **Network Connectivity**
   ```bash
   # Test PubChem connectivity
   curl -I https://pubchem.ncbi.nlm.nih.gov/
   
   # Check DNS resolution
   nslookup pubchem.ncbi.nlm.nih.gov
   
   # Test with Python
   python -c "import urllib.request; print(urllib.request.urlopen('https://pubchem.ncbi.nlm.nih.gov/', timeout=10).getcode())"
   ```

3. **Increase Timeout Values**
   ```python
   # In the notebook, modify timeout in Cell 3
   with urllib.request.urlopen(url, timeout=30) as request:  # Increase from 20 to 30
   ```

4. **Handle Special Characters**
   ```python
   # Add to name processing in get_cid_and_smiles function
   def clean_compound_name(name):
       # Remove extra spaces and special characters
       cleaned = re.sub(r'\s+', ' ', name.strip())
       # Handle common problematic characters
       cleaned = cleaned.replace('−', '-')  # Replace minus with hyphen
       cleaned = cleaned.replace('–', '-')  # Replace en-dash with hyphen
       return cleaned
   ```

#### Issue: Certificate/SSL Errors
**Symptoms:**
- SSL certificate verification errors
- Connection refused errors
- HTTPS handshake failures

**Solutions:**
1. **Update Certificates**
   ```bash
   pip install --upgrade certifi
   pip install --upgrade urllib3
   ```

2. **Check System Time**
   ```bash
   # Ensure system clock is correct
   date  # Linux/macOS
   time  # Windows
   ```

3. **Bypass SSL (Last Resort)**
   ```python
   import ssl
   import urllib.request
   
   # Create unverified context
   ssl_context = ssl.create_default_context()
   ssl_context.check_hostname = False
   ssl_context.verify_mode = ssl.CERT_NONE
   
   # Use in requests
   urllib.request.urlopen(url, context=ssl_context)
   ```

#### Issue: Rate Limiting
**Symptoms:**
- "Too many requests" errors
- Sudden drop in success rate
- HTTP 429 errors

**Solutions:**
1. **Increase Delay Between Requests**
   ```python
   # Modify in Cell 4
   time.sleep(1.0)  # Increase from 0.5 to 1.0 seconds
   ```

2. **Implement Exponential Backoff**
   ```python
   import random
   
   def make_request_with_backoff(url, max_retries=3):
       for attempt in range(max_retries):
           try:
               # Add randomness to avoid thundering herd
               delay = 0.5 + random.uniform(0, 0.5) * (attempt + 1)
               time.sleep(delay)
               
               with urllib.request.urlopen(url, timeout=30) as response:
                   return response.read()
           except urllib.error.HTTPError as e:
               if e.code == 429:  # Rate limited
                   wait_time = 2 ** attempt + random.uniform(0, 1)
                   time.sleep(wait_time)
               else:
                   raise
       raise Exception("Max retries exceeded")
   ```

### ChromeDriver Issues

#### Issue: ChromeDriver Version Mismatch
**Symptoms:**
- "This version of ChromeDriver only supports Chrome version X"
- Browser fails to start
- Selenium WebDriver exceptions

**Solutions:**
1. **Check Chrome Version**
   ```bash
   # Windows
   reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version
   
   # Linux
   google-chrome --version
   chromium-browser --version
   
   # macOS
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
   ```

2. **Update ChromeDriver Automatically**
   ```bash
   pip install --upgrade webdriver-manager
   ```

3. **Manual ChromeDriver Update**
   ```python
   # Check current ChromeDriver version
   from selenium import webdriver
   from selenium.webdriver.chrome.service import Service
   
   service = Service()
   driver = webdriver.Chrome(service=service)
   capabilities = driver.capabilities
   print(f"ChromeDriver version: {capabilities['chrome']['chromedriverVersion']}")
   print(f"Chrome version: {capabilities['browserVersion']}")
   driver.quit()
   ```

4. **Force Specific ChromeDriver Version**
   ```python
   from webdriver_manager.chrome import ChromeDriverManager
   
   # Install specific version
   driver_path = ChromeDriverManager(version="114.0.5735.90").install()
   service = Service(driver_path)
   ```

#### Issue: ChromeDriver Not Found
**Symptoms:**
- "chromedriver not found in PATH"
- "No such file or directory: chromedriver"
- WebDriverException on initialization

**Solutions:**
1. **Verify File Permissions**
   ```bash
   # Linux/macOS
   chmod +x chromedriver
   ls -la chromedriver
   
   # Test execution
   ./chromedriver --version
   ```

2. **Check PATH Environment**
   ```bash
   # Windows
   echo %PATH%
   
   # Linux/macOS
   echo $PATH
   
   # Check if chromedriver is in PATH
   which chromedriver
   ```

3. **Use Absolute Path in Script**
   ```python
   # Modify swisstarget.py
   import os
   
   def get_chromedriver_path():
       possible_paths = [
           './chromedriver',
           './chromedriver.exe',
           '/usr/local/bin/chromedriver',
           '/usr/bin/chromedriver'
       ]
       
       for path in possible_paths:
           if os.path.exists(path):
               return path
       
       return None
   
   # Use in setup_webdriver function
   chromedriver_path = get_chromedriver_path()
   if chromedriver_path:
       service = Service(executable_path=chromedriver_path)
   ```

#### Issue: Chrome Browser Not Found
**Symptoms:**
- "Chrome binary not found"
- Browser fails to launch
- Path-related errors

**Solutions:**
1. **Install Google Chrome**
   ```bash
   # Ubuntu/Debian
   wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
   sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
   sudo apt-get update
   sudo apt-get install google-chrome-stable
   
   # CentOS/RHEL
   sudo yum install google-chrome-stable
   ```

2. **Specify Chrome Binary Path**
   ```python
   # Add to setup_webdriver function
   chrome_paths = [
       "/usr/bin/google-chrome",
       "/usr/bin/chromium-browser",
       "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
       "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
       "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
   ]
   
   for path in chrome_paths:
       if os.path.exists(path):
           chrome_options.binary_location = path
           break
   ```

3. **Use Chrome Beta/Dev/Canary**
   ```python
   # Alternative Chrome versions
   chrome_options.binary_location = "/usr/bin/google-chrome-beta"
   # or
   chrome_options.binary_location = "/usr/bin/google-chrome-unstable"
   ```

### SwissTarget Website Issues

#### Issue: Website Structure Changes
**Symptoms:**
- Element not found errors
- Timeout waiting for elements
- Unexpected page layouts

**Solutions:**
1. **Update Element Selectors**
   ```python
   # Add fallback selectors
   def find_element_robust(driver, primary_selector, fallback_selectors=None):
       try:
           return driver.find_element(By.ID, primary_selector)
       except:
           if fallback_selectors:
               for selector_type, selector_value in fallback_selectors:
                   try:
                       return driver.find_element(selector_type, selector_value)
                   except:
                       continue
           raise Exception(f"Element not found with any selector")
   
   # Usage example
   smiles_input = find_element_robust(
       driver, 
       "smilesBox",
       [(By.NAME, "smiles"), (By.CSS_SELECTOR, "input[type='text']")]
   )
   ```

2. **Increase Wait Times**
   ```python
   # Modify timeouts in swisstarget.py
   def wait_for_element(driver, selector, timeout=60):
       try:
           element = WebDriverWait(driver, timeout).until(
               EC.presence_of_element_located((By.ID, selector))
           )
           return element
       except TimeoutException:
           # Take screenshot for debugging
           driver.save_screenshot(f"timeout_error_{selector}.png")
           raise
   ```

3. **Check Website Accessibility**
   ```python
   import requests
   
   def check_website_status():
       try:
           response = requests.get("http://www.swisstargetprediction.ch/", timeout=30)
           if response.status_code == 200:
               print("✅ Website is accessible")
               return True
           else:
               print(f"⚠️ Website returned status code: {response.status_code}")
               return False
       except Exception as e:
           print(f"❌ Website check failed: {e}")
           return False
   ```

#### Issue: Prediction Failures
**Symptoms:**
- Results table never loads
- "No targets found" messages
- Blank result pages

**Solutions:**
1. **Verify SMILES Format**
   ```python
   # Add SMILES validation
   def validate_smiles(smiles):
       try:
           # Basic SMILES validation
           if not smiles or len(smiles.strip()) == 0:
               return False, "Empty SMILES"
           
           # Check for common invalid characters
           invalid_chars = ['<', '>', '"', "'", '\\', '|']
           for char in invalid_chars:
               if char in smiles:
                   return False, f"Invalid character: {char}"
           
           # Check basic structure
           if not any(c.isalpha() for c in smiles):
               return False, "No atoms found"
           
           return True, "Valid"
       except Exception as e:
           return False, f"Validation error: {e}"
   
   # Use before prediction
   is_valid, message = validate_smiles(smiles)
   if not is_valid:
       write_log(f"❌ Invalid SMILES: {message}")
       return None
   ```

2. **Handle Different Result Formats**
   ```python
   def wait_for_results(driver, timeout=240):
       # Try multiple result indicators
       result_selectors = [
           (By.ID, "results_table"),
           (By.CSS_SELECTOR, "table.display"),
           (By.CLASS_NAME, "dataTables_wrapper"),
           (By.XPATH, "//table[contains(@class, 'dataTable')]")
       ]
       
       for selector_type, selector_value in result_selectors:
           try:
               element = WebDriverWait(driver, timeout).until(
                   EC.presence_of_element_located((selector_type, selector_value))
               )
               write_log(f"✅ Results found with selector: {selector_type} = {selector_value}")
               return element
           except TimeoutException:
               continue
       
       # Check for error messages
       error_selectors = [
           (By.CLASS_NAME, "error"),
           (By.ID, "error_message"),
           (By.XPATH, "//div[contains(text(), 'error')]")
       ]
       
       for selector_type, selector_value in error_selectors:
           try:
               error_element = driver.find_element(selector_type, selector_value)
               if error_element.is_displayed():
                   error_text = error_element.text
                   raise Exception(f"Website error: {error_text}")
           except:
               continue
       
       raise Exception("No results found with any selector")
   ```

### Memory and Performance Issues

#### Issue: High Memory Usage
**Symptoms:**
- System becomes slow during processing
- Python process uses excessive RAM
- Browser crashes or freezes

**Solutions:**
1. **Optimize Browser Options**
   ```python
   def setup_optimized_webdriver():
       chrome_options = Options()
       
       # Memory optimization
       chrome_options.add_argument("--max_old_space_size=4096")
       chrome_options.add_argument("--memory-pressure-off")
       chrome_options.add_argument("--disable-background-timer-throttling")
       chrome_options.add_argument("--disable-renderer-backgrounding")
       chrome_options.add_argument("--disable-backgrounding-occluded-windows")
       
       # Disable unnecessary features
       chrome_options.add_argument("--disable-images")
       chrome_options.add_argument("--disable-javascript")  # Use only if site works without JS
       chrome_options.add_argument("--disable-plugins")
       chrome_options.add_argument("--disable-extensions")
       
       return chrome_options
   ```

2. **Process in Batches**
   ```python
   def process_compounds_in_batches(df, batch_size=10):
       total_compounds = len(df)
       
       for i in range(0, total_compounds, batch_size):
           batch = df.iloc[i:i+batch_size]
           write_log(f"Processing batch {i//batch_size + 1}: compounds {i+1} to {min(i+batch_size, total_compounds)}")
           
           for index, row in batch.iterrows():
               # Process compound
               result = predict_swisstarget_locally(row['Name'], row['Smiles'], output_path)
               
               # Clean up between compounds
               time.sleep(2)
           
           # Longer break between batches
           if i + batch_size < total_compounds:
               write_log("⏸️ Batch completed. Resting for 10 seconds...")
               time.sleep(10)
   ```

3. **Monitor Resource Usage**
   ```python
   import psutil
   
   def log_system_resources():
       cpu_percent = psutil.cpu_percent(interval=1)
       memory = psutil.virtual_memory()
       
       write_log(f"💻 System resources:")
       write_log(f"   CPU: {cpu_percent}%")
       write_log(f"   Memory: {memory.percent}% ({memory.used // 1024 // 1024} MB used)")
       
       if memory.percent > 80:
           write_log("⚠️ High memory usage detected")
       if cpu_percent > 90:
           write_log("⚠️ High CPU usage detected")
   ```

### Data Quality Issues

#### Issue: Inconsistent Input Data
**Symptoms:**
- Some compounds processed, others skipped
- Encoding errors in compound names
- Missing or malformed SMILES

**Solutions:**
1. **Enhanced Data Validation**
   ```python
   def comprehensive_data_validation(df):
       write_log("🔍 Performing comprehensive data validation...")
       
       issues = []
       
       # Check for required columns
       required_cols = ['Name', 'Smiles']
       missing_cols = [col for col in required_cols if col not in df.columns]
       if missing_cols:
           issues.append(f"Missing columns: {missing_cols}")
       
       # Check for empty values
       for col in required_cols:
           if col in df.columns:
               empty_count = df[col].isna().sum() + (df[col] == '').sum()
               if empty_count > 0:
                   issues.append(f"Empty values in {col}: {empty_count}")
       
       # Check for duplicate names
       if 'Name' in df.columns:
           duplicates = df['Name'].duplicated().sum()
           if duplicates > 0:
               issues.append(f"Duplicate names: {duplicates}")
       
       # Check SMILES format
       if 'Smiles' in df.columns:
           invalid_smiles = 0
           for smiles in df['Smiles'].dropna():
               if not isinstance(smiles, str) or len(smiles.strip()) == 0:
                   invalid_smiles += 1
           if invalid_smiles > 0:
               issues.append(f"Invalid SMILES format: {invalid_smiles}")
       
       # Report issues
       if issues:
           write_log("❌ Data validation issues found:")
           for issue in issues:
               write_log(f"   - {issue}")
           return False
       else:
           write_log("✅ Data validation passed")
           return True
   ```

2. **Handle Encoding Issues**
   ```python
   def fix_encoding_issues(df):
       write_log("🔧 Fixing encoding issues...")
       
       for col in df.columns:
           if df[col].dtype == 'object':
               # Fix common encoding issues
               df[col] = df[col].astype(str)
               df[col] = df[col].str.replace('â', 'α')
               df[col] = df[col].str.replace('Î²', 'β')
               df[col] = df[col].str.replace('Î³', 'γ')
               
               # Remove non-printable characters
               df[col] = df[col].str.replace(r'[^\x20-\x7E]', '', regex=True)
       
       return df
   ```

### Debugging and Logging

#### Issue: Insufficient Debugging Information
**Symptoms:**
- Hard to identify where process fails
- No intermediate files for troubleshooting
- Unclear error messages

**Solutions:**
1. **Enhanced Logging**
   ```python
   import logging
   
   def setup_detailed_logging():
       logging.basicConfig(
           level=logging.DEBUG,
           format='%(asctime)s - %(levelname)s - %(message)s',
           handlers=[
               logging.FileHandler('detailed_debug.log'),
               logging.StreamHandler()
           ]
       )
       
       # Log system information
       import platform
       logging.info(f"Python version: {platform.python_version()}")
       logging.info(f"Operating system: {platform.system()} {platform.release()}")
       
       # Log package versions
       try:
           import selenium
           logging.info(f"Selenium version: {selenium.__version__}")
       except:
           logging.warning("Selenium version not available")
   ```

2. **Create Debug Checkpoint Files**
   ```python
   def save_debug_checkpoint(df, stage, folder):
       checkpoint_file = os.path.join(folder, f"debug_checkpoint_{stage}.csv")
       df.to_csv(checkpoint_file, index=False)
       write_log(f"🔍 Debug checkpoint saved: {checkpoint_file}")
   ```

3. **Screenshot on Errors**
   ```python
   def capture_debug_screenshot(driver, error_description, output_folder):
       timestamp = datetime.now().strftime("%H%M%S")
       screenshot_path = os.path.join(output_folder, f"debug_{timestamp}_{error_description}.png")
       
       try:
           driver.save_screenshot(screenshot_path)
           
           # Also save page source
           source_path = os.path.join(output_folder, f"debug_{timestamp}_{error_description}.html")
           with open(source_path, 'w', encoding='utf-8') as f:
               f.write(driver.page_source)
           
           write_log(f"📸 Debug files saved: {screenshot_path}")
           return screenshot_path
       except Exception as e:
           write_log(f"❌ Failed to capture debug screenshot: {e}")
           return None
   ```

### Performance Optimization

#### Issue: Slow Processing Speed
**Symptoms:**
- Long wait times between compounds
- Timeouts during processing
- Inefficient resource usage

**Solutions:**
1. **Optimize Wait Strategies**
   ```python
   from selenium.webdriver.support.wait import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   
   def smart_wait(driver, selector, timeout=30):
       """Smart wait that combines multiple strategies"""
       try:
           # First try explicit wait
           element = WebDriverWait(driver, timeout).until(
               EC.presence_of_element_located((By.ID, selector))
           )
           return element
       except TimeoutException:
           # If that fails, try polling
           for _ in range(timeout):
               try:
                   element = driver.find_element(By.ID, selector)
                   if element.is_displayed():
                       return element
               except:
                   pass
               time.sleep(1)
           raise TimeoutException(f"Element {selector} not found after {timeout} seconds")
   ```

2. **Implement Connection Pooling**
   ```python
   import urllib3
   
   def setup_connection_pool():
       http = urllib3.PoolManager(
           num_pools=10,
           maxsize=10,
           timeout=urllib3.Timeout(connect=10, read=30)
       )
       return http
   ```

3. **Parallel Processing (Advanced)**
   ```python
   from concurrent.futures import ThreadPoolExecutor
   import queue
   
   def process_compounds_parallel(df, max_workers=2):
       """Process compounds in parallel (use carefully with web scraping)"""
       results_queue = queue.Queue()
       
       def process_compound(compound_data):
           name, smiles = compound_data
           result = predict_swisstarget_locally(name, smiles, output_path)
           results_queue.put((name, result))
           return result
       
       compound_data = [(row['Name'], row['Smiles']) for _, row in df.iterrows()]
       
       with ThreadPoolExecutor(max_workers=max_workers) as executor:
           futures = [executor.submit(process_compound, data) for data in compound_data]
           
           for future in futures:
               try:
                   result = future.result(timeout=300)  # 5 minute timeout
               except Exception as e:
                   write_log(f"❌ Parallel processing error: {e}")
   ```

## Quick Fix Checklist

When things go wrong, try these quick fixes in order:

### 🔥 Emergency Fixes (Try First)

1. **Restart Everything**
   ```bash
   # Kill all Chrome processes
   pkill -f chrome
   # Restart Python kernel/script
   ```

2. **Check Internet Connection**
   ```bash
   ping google.com
   curl -I https://pubchem.ncbi.nlm.nih.gov/
   ```

3. **Update Dependencies**
   ```bash
   pip install --upgrade selenium webdriver-manager pandas
   ```

4. **Clear Browser Cache**
   ```python
   chrome_options.add_argument("--disable-cache")
   chrome_options.add_argument("--aggressive-cache-discard")
   ```

### 📋 Systematic Troubleshooting

1. **Data Issues** → Check CSV format, column names, encoding
2. **Network Issues** → Check connectivity, timeouts, rate limiting
3. **Browser Issues** → Update ChromeDriver, check Chrome version
4. **Website Issues** → Check site accessibility, element selectors
5. **Memory Issues** → Reduce batch size, optimize browser options
6. **Performance Issues** → Increase timeouts, optimize wait strategies

### 🆘 Last Resort

If nothing else works:
1. Run with minimal data (1-2 compounds)
2. Use verbose logging and debugging
3. Check GitHub issues for similar problems
4. Contact support with detailed logs

---

**Remember**: Most issues are related to version mismatches, network problems, or website structure changes. Always check the basics first!
