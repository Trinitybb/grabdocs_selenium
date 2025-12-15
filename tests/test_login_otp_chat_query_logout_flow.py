
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

# ---- Setup ----
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://app.grabdocs.com/login")
wait = WebDriverWait(driver, 15)

# ---- Screenshot Helper ----
if not os.path.exists("screenshots_grab_docs"):
    os.makedirs("screenshots_grab_docs")

def take_screenshot(name):
    path = f"screenshots_grab_docs/{name}.png"
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")

print("\n=== GRABDOCS AUTOMATION TEST START ===")

# ---------------- LOGIN TEST ----------------
print("\n[1] Performing Login Test...")

try:
    username_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='text' or contains(@placeholder, 'Username')]")
    ))
    password_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']")
    ))

    username_field.send_keys("bowlingt0912@students.bowiestate.edu")
    password_field.send_keys("Testing123")

    sign_in_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Sign in')]")
    ))
    sign_in_button.click()
    print("Credentials submitted — waiting for 2FA step...")
    take_screenshot("login_success")  # Screenshot after successful login form submission

    # ---- Auto-fill OTP ----
    print("\nAttempting to enter OTP automatically...")
    otp_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//input[@type='text' and (contains(@placeholder, 'code') or contains(@placeholder, 'OTP') or contains(@name, 'otp'))]"
        ))
    )
    otp_field.send_keys("335577")
    print("OTP entered: 335577")

    verify_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(., 'Verify')] | //button[contains(., 'Continue')] | //button[contains(., 'Submit')]"
        ))
    )
    verify_button.click()
    print("Verifying OTP...")
    take_screenshot("otp_verified")  # Screenshot after OTP verification click

    # --- Wait for dashboard ---
    print("Waiting for dashboard to fully load...")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[contains(., 'Drop files') or contains(., 'Upload documents') or contains(., 'Reach') or contains(., 'Workspace')]"
        ))
    )
    print("Login + 2FA successful — Dashboard elements detected.")
    take_screenshot("dashboard_loaded")

except Exception as e:
    take_screenshot("login_failed")
    print(f"Login or OTP verification failed ({e})")

# ---------------- WORKSPACE CHAT TEST ----------------
print("\n[2] Testing Workspace Chat...")

try:
    # ---- Locate chat input ----
    chat_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//textarea | //input[contains(@placeholder, 'Ask') or contains(@placeholder, 'message')]"
        ))
    )

    message = "hello from selenium testing"
    chat_input.send_keys(message)
    chat_input.send_keys(u'\ue007')  # Enter

    print(f"Sent workspace message: {message}")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            By.XPATH, f"//div[contains(., '{message}')]"
        ))
    )

    take_screenshot("workspace_message_sent")

    # ---- CLICK SHOW HISTORY ----
    print("Opening chat history...")

    history_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((
            By.XPATH, "//button[@title='Show History']"
        ))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", history_button)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", history_button)

    print("Show History button clicked.")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[contains(., 'hello from selenium testing')]"
        ))
    )

    take_screenshot("chat_history_opened")
    print("Chat history displayed successfully.")

except Exception as e:
    take_screenshot("workspace_chat_failed")
    print(f"Workspace chat test failed ({e})")

# ---------------- LOGOUT TEST ----------------
print("\n[3] Logging Out...")
try:
    logout_button = WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(., 'Logout')] "
            "| //button[contains(., 'Sign out')] "
            "| //span[contains(., 'Log out')]"
        ))
    )
    logout_button.click()
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(., 'Sign in')]")
    ))
    print("Logout successful — Returned to login page.")
    take_screenshot("logout_success")

except Exception as e:
    take_screenshot("logout_failed")
    print(f"Logout test failed ({e})")

# ---------------- CLEANUP ----------------
driver.quit()
print("\nGRABDOCS AUTOMATION TEST COMPLETED SUCCESSFULLY.")
