# swisstarget.py --> terminal => python swisstarget.py
import pandas as pd
import os
import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
main_folder_name = f"swisstarget_results_{timestamp}"
os.makedirs(main_folder_name, exist_ok=True)
log_file_path = os.path.join(main_folder_name, "process_log.txt")


def write_log(message):
    log_message = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
    print(log_message)
    with open(log_file_path, "a", encoding='utf-8') as f:
        f.write(log_message + "\n")


# --- 2. Setup WebDriver with Robust Configuration ---
def setup_webdriver():
    """Setup WebDriver with more stable configuration"""
    try:
        chrome_options = Options()
        # Add options for stability and avoiding bot detection
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        driver = None
        try:
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            write_log("✅ WebDriver initialized successfully using ChromeDriverManager.")
        except Exception as e_w_m:
            write_log(f"⚠️ Failed to initialize with ChromeDriverManager: {e_w_m}. Trying local chromedriver.exe...")
            try:
                service = ChromeService(executable_path='chromedriver.exe')
                driver = webdriver.Chrome(service=service, options=chrome_options)
                write_log("✅ WebDriver initialized successfully using local chromedriver.exe.")
            except Exception as e_local:
                write_log(f"⚠️ Failed to initialize with local chromedriver.exe: {e_local}. Trying from PATH...")
                try:
                    driver = webdriver.Chrome(options=chrome_options)
                    write_log("✅ WebDriver initialized successfully from PATH.")
                except Exception as e_path:
                    write_log(f"❌ FAILED to start WebDriver from PATH: {e_path}")
                    raise

        if driver:
            driver.implicitly_wait(1)
            return driver
        else:
            return None
    except Exception as e:
        write_log(f"❌ FAILED to initialize WebDriver: {e}")
        write_log("💡 Make sure:")
        write_log("   - chromedriver.exe is in the same folder, OR")
        write_log("   - Install webdriver-manager: pip install webdriver-manager, OR")
        write_log("   - ChromeDriver is available in system PATH and version matches.")
        return None


# --- 3. SwissTarget Prediction Function with Retry Mechanism ---
def predict_swisstarget_locally(compound_name, smiles, output_folder, max_retries=3):
    """Run SwissTargetPrediction with retry mechanism"""
    os.makedirs(output_folder, exist_ok=True)
    for attempt in range(max_retries):
        driver = None
        try:
            write_log(f"🔎 Starting prediction for: '{compound_name}' (Attempt {attempt + 1}/{max_retries})...")
            driver = setup_webdriver()
            if driver is None:
                write_log(f"❌ Cannot get WebDriver. Skipping '{compound_name}'.")
                return None

            write_log("   📡 Accessing SwissTargetPrediction website...")
            driver.set_page_load_timeout(60)
            driver.get("http://www.swisstargetprediction.ch/")

            write_log("   ⏳ Waiting for SMILES input field (ID: 'smilesBox') to appear and be clickable...")
            smiles_input = None
            try:
                smiles_input = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "smilesBox"))
                )
                write_log("   ✅ SMILES input field (ID: 'smilesBox') found and ready.")
            except TimeoutException:
                write_log("   ❌ Timeout: SMILES input field not found or not clickable within 30 seconds.")
                raise Exception("SMILES input field with ID 'smilesBox' not found. Page structure may have changed.")

            time.sleep(1)

            write_log("   👤 Ensuring 'Homo sapiens' is selected...")
            try:
                homo_sapiens_radio = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='organism' and @value='Homo_sapiens']"))
                )
                if not homo_sapiens_radio.is_selected():
                    try:
                        homo_sapiens_radio.click()
                        write_log("   ✅ 'Homo sapiens' selected via direct click.")
                    except WebDriverException:
                        write_log("   ⚠️ Direct click failed. Trying JavaScript click for 'Homo sapiens'.")
                        driver.execute_script("arguments[0].click();", homo_sapiens_radio)
                        write_log("   ✅ 'Homo sapiens' selected via JavaScript.")
                else:
                    write_log("   ✅ 'Homo sapiens' already selected by default.")
            except TimeoutException:
                write_log("   ❌ Timeout: Radio button 'Homo sapiens' not found within 10 seconds.")
            except Exception as e:
                write_log(f"   ⚠️ Failed to select 'Homo sapiens': {type(e).__name__}: {e}")

            write_log(f"   ✏️ Filling SMILES '{smiles}' via JavaScript...")
            driver.execute_script("arguments[0].value = arguments[1];", smiles_input, smiles)
            write_log("   ✅ SMILES filled successfully.")
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", smiles_input)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", smiles_input)
            time.sleep(2)

            write_log("   🚀 Submitting prediction request: Trying to click button via JavaScript...")
            submit_button = None
            try:
                submit_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "submitButton"))
                )
                write_log("   ✅ 'Predict targets' button (ID: 'submitButton') found in DOM.")
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(0.5)
                driver.execute_script("formSubmit();")
                write_log("   ✅ JavaScript function 'formSubmit()' called successfully.")
            except TimeoutException:
                write_log("   ❌ Timeout: 'Predict targets' button not found in DOM.")
                driver.save_screenshot(os.path.join(output_folder, f"error_button_not_found_attempt_{attempt + 1}.png"))
                raise Exception("Predict targets button not found in DOM.")
            except Exception as e:
                write_log(f"   ❌ Failed to click 'Predict targets' via JavaScript: {type(e).__name__}: {e}")
                driver.save_screenshot(os.path.join(output_folder, f"error_js_click_attempt_{attempt + 1}.png"))
                raise Exception(f"Error interacting with 'Predict targets' button via JavaScript: {e}")

            write_log("   ⏳ Waiting for results table to load...")
            results_table = None
            try:
                results_table = WebDriverWait(driver, 240).until(
                    EC.presence_of_element_located((By.ID, "results_table"))
                )
                write_log("   ✅ Results table loaded (ID: results_table)")
            except TimeoutException:
                write_log("   ❌ Timeout: Results table not loaded within 240 seconds. Trying CSS selector...")
                try:
                    results_table = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table.display"))
                    )
                    write_log("   ✅ Results table found using CSS selector 'table.display'.")
                except TimeoutException:
                    raise Exception("Timeout waiting for results - server might be slow, SMILES invalid, or page structure changed.")

            # --- START: MANUAL INTERACTION SECTION ---
            write_log(f"\n{'=' * 60}")
            write_log(f"✨✨ ANALYSIS FOR '{compound_name}' COMPLETED AND DISPLAYED IN BROWSER ✨✨")
            write_log(f"📁 Output folder prepared at: '{output_folder}'")
            write_log("")
            write_log("❗ PLEASE DOWNLOAD FILES (CSV/Excel/PDF) AND TAKE SCREENSHOTS MANUALLY.")
            write_log(f"   Save files into folder: '{os.path.abspath(output_folder)}'")
            write_log("")
            write_log("⏩ After finishing, please CLOSE THE BROWSER MANUALLY.")
            write_log("   The program will detect browser closure and continue to next compound.")
            write_log(f"\n{'=' * 60}")
            # Wait until user closes the browser manually
            while True:
                try:
                    driver.current_url
                    time.sleep(1)
                except WebDriverException:
                    write_log(f"✅ Browser for '{compound_name}' closed. Proceeding to next compound...")
                    break
            return True
        except Exception as e:
            write_log(f"   ❌ Prediction failed for '{compound_name}' (Attempt {attempt + 1}): {type(e).__name__}: {e}")
            if driver:
                error_screenshot_path = os.path.join(output_folder, f"error_screenshot_attempt_{attempt + 1}.png")
                try:
                    driver.save_screenshot(error_screenshot_path)
                    write_log(f"   📸 Error screenshot saved at: {error_screenshot_path}")
                except Exception as screenshot_e:
                    write_log(f"   ⚠️ Failed to save error screenshot: {screenshot_e}")
        finally:
            if driver:
                driver.quit()
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 1
            write_log(f"   🔁 Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            write_log(f"   ❌ All attempts failed for '{compound_name}'")
            return None
    return None


# --- 4. Input Validation Function ---
def validate_input_file(file_path):
    """Validate input file and required columns"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found")
        df = pd.read_csv(file_path, sep=',')
        required_columns = ['Name', 'Smiles']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            write_log(f"❌ Missing columns: {missing_columns}")
            write_log(f"   Available columns: {list(df.columns)}")
            return None
        write_log(f"✅ Input file valid: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        write_log(f"❌ Error validating input file: {e}")
        return None


# --- 5. Main Process Function ---
def main():
    write_log("=" * 60)
    write_log("--- SWISSTARGET PREDICTION PROCESS STARTED ---")
    write_log("=" * 60)
    input_file = 'data_compounds_final_full.csv'
    df_input = validate_input_file(input_file)
    if df_input is None:
        write_log("❌ Process stopped due to input file issue")
        return

    df_valid = df_input.dropna(subset=['Smiles']).copy()
    df_valid = df_valid[df_valid['Smiles'].str.strip() != '']

    write_log(f"📊 Data statistics:")
    write_log(f"   Total compounds: {len(df_input)}")
    write_log(f"   Compounds with valid SMILES: {len(df_valid)}")
    if len(df_valid) == 0:
        write_log("❌ No compounds with valid SMILES to process")
        return

    success_count = 0
    fail_count = 0

    for index, row in df_valid.iterrows():
        name = str(row['Name']).strip()
        smiles = str(row['Smiles']).strip()
        write_log(f"\n{'=' * 40}")
        write_log(f"Processing compound {index + 1}/{len(df_valid)}: {name}")
        write_log(f"SMILES: {smiles}")
        safe_folder_name = re.sub(r'[\\/*?:"<>|]', "_", name)[:100]
        output_path = os.path.join(main_folder_name, f"{index+1:03d}_{safe_folder_name}")
        result = predict_swisstarget_locally(name, smiles, output_path)
        if result:
            success_count += 1
            write_log(f"✅ Processing succeeded for: {name}. Waiting for browser to close.")
        else:
            fail_count += 1
            write_log(f"❌ Processing failed for: {name}. Proceeding to next compound.")
        if index < len(df_valid) - 1:
            write_log("⏳ Waiting 5 seconds before next compound...")
            time.sleep(1)

    write_log(f"\n{'=' * 60}")
    write_log("FINAL SUMMARY:")
    write_log(f"✅ Successfully processed compounds (waiting for manual input): {success_count}")
    write_log(f"❌ Failed compounds: {fail_count}")
    write_log(f"📊 Total compounds tried: {success_count + fail_count}")
    write_log(f"\n{'=' * 60}")
    write_log("✨ SWISSTARGET PREDICTION PROCESS COMPLETED")
    write_log(f"{'=' * 60}")


# --- 6. Run the Program ---
if __name__ == "__main__":
    main()