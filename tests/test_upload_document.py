
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


# ---- Config ----
USERNAME = "barbietrin4eva@gmail.com"
PASSWORD = "testing123!"
OTP_CODE = "335577"

# File to upload (PersonalStatement.docx lives in the same folder as this script)
HERE = os.path.dirname(os.path.abspath(__file__))
FILE_TO_UPLOAD = os.path.join(HERE, "PersonalStatement.docx")

# ---- Setup ----
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://app.grabdocs.com/login")
wait = WebDriverWait(driver, 20)

# ---- Screenshot Helper ----
if not os.path.exists("screenshots_grab_docs"):
    os.makedirs("screenshots_grab_docs")


def take_screenshot(name: str) -> None:
    path = f"screenshots_grab_docs/{name}.png"
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")


print("\n=== GRABDOCS UPLOAD TEST START ===")

# ---------------- LOGIN + OTP ----------------
print("\n[1] Logging In...")
try:
    username_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='text' and not(contains(@placeholder, 'code'))]")
    ))
    password_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']")
    ))

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    sign_in_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Sign in')]")
    ))
    sign_in_button.click()
    take_screenshot("upload_login_submitted")

    otp_field = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//input[contains(@placeholder, 'code') or contains(@placeholder, 'Code') or contains(@name, 'otp') or contains(@id, 'otp')]"
        ))
    )
    otp_field.send_keys(OTP_CODE)

    verify_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(., 'Verify')] | //button[contains(., 'Continue')] | //button[contains(., 'Submit')]"
        ))
    )
    verify_button.click()
    take_screenshot("upload_otp_submitted")

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((
            By.XPATH, "//div[contains(., 'Drop files') or contains(., 'Workspace')]"
        ))
    )
    take_screenshot("upload_dashboard_loaded")
    print("Login and OTP successful.")

except Exception as e:
    take_screenshot("upload_login_failed")
    print(f"Login failed: {e}")
    driver.quit()
    raise SystemExit(1)


# ---------------- NAVIGATE TO UPLOAD ----------------
print("\n[2] Opening Upload Page...")
try:
    driver.get("https://app.grabdocs.com/upload")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH, "//div[contains(., 'Drop files') or @role='presentation' or @data-testid='dropzone']"
        ))
    )
    take_screenshot("upload_page_loaded")
except Exception as e:
    take_screenshot("upload_page_failed")
    print(f"Upload page did not load: {e}")
    driver.quit()
    raise SystemExit(1)


# ---------------- UPLOAD FILE ----------------
print("\n[3] Uploading DOCX file...")
if not os.path.exists(FILE_TO_UPLOAD):
    print(f"File to upload not found: {FILE_TO_UPLOAD}")
    driver.quit()
    raise SystemExit(1)

try:
    upload_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    upload_input.send_keys(FILE_TO_UPLOAD)
    print(f"File selected: {FILE_TO_UPLOAD}")
    take_screenshot("upload_file_selected")

    file_name_snippet = os.path.basename(FILE_TO_UPLOAD).split(".")[0]
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((
            By.XPATH,
            f"//div[contains(., '{file_name_snippet}')] | //span[contains(., '{file_name_snippet}')]"
        ))
    )
    print("Upload completed and file appeared in the list.")
    take_screenshot("upload_completed")

except Exception as e:
    take_screenshot("upload_failed")
    print(f"Upload failed: {e}")
    driver.quit()
    raise SystemExit(1)


# ---------------- VERIFY IN FILES PAGE ----------------
print("\n[4] Verifying file in Files page...")
try:
    # Use direct nav to the Files page for consistency
    driver.get("https://app.grabdocs.com/files")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            By.XPATH, "(//div[contains(., 'Quick Files')] | //h1[contains(., 'Files')])[1]"
        ))
    )

    file_name_snippet = os.path.basename(FILE_TO_UPLOAD).split(".")[0]
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((
            By.XPATH,
            f"//div[contains(., '{file_name_snippet}')] | //span[contains(., '{file_name_snippet}')]"
        ))
    )
    print("File visible on Files page.")
    take_screenshot("upload_file_listed")
except Exception as e:
    take_screenshot("upload_file_not_listed")
    print(f"File not visible on Files page: {e}")
    driver.quit()
    raise SystemExit(1)


# ---------------- LOGOUT ----------------
print("\n[5] Logging Out...")
try:
    profile_or_logout = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(., 'Logout')] "
            "| //button[contains(., 'Sign out')] "
            "| //span[contains(., 'Log out')] "
            "| //div[contains(@class, 'profile') or contains(@class, 'avatar')][1]"
        ))
    )
    profile_or_logout.click()

    logout_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(., 'Logout')] | //button[contains(., 'Sign out')] | //span[contains(., 'Log out')]"
        ))
    )
    logout_button.click()

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(., 'Sign in')]")
    ))
    print("Logout successful.")
    take_screenshot("upload_logout_success")
except Exception as e:
    take_screenshot("upload_logout_failed")
    print(f"Logout failed: {e}")


# ---------------- CLEANUP ----------------
driver.quit()
print("\nGRABDOCS UPLOAD TEST COMPLETED SUCCESSFULLY.")
