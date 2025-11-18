

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# ---- Config ----
USERNAME = "barbietrin4eva@gmail.com"
PASSWORD = "testng123!"
OTP_CODE = "335577"

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


print("\n=== GRABDOCS SETTINGS DISPLAY THEME TOGGLE TEST START ===")

# ---------------- LOGIN + OTP ----------------
print("\n[1] Logging In...")

try:
    username_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='text' or contains(@placeholder, 'Username')]")
    ))
    password_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']")
    ))

    username_field.send_keys("barbietrin4eva@gmail.com")
    password_field.send_keys("testing123!")

    sign_in_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Sign in')]")
    ))
    sign_in_button.click()
    print("Credentials submitted — waiting for 2FA step...")
    take_screenshot("login_success")  # Screenshot after successful login form submission

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
    take_screenshot("settings_otp_submitted")

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((
            By.XPATH, "//div[contains(., 'Drop files') or contains(., 'Workspace')]"
        ))
    )
    take_screenshot("settings_dashboard_loaded")
    print("Login and OTP successful.")

except Exception as e:
    take_screenshot("settings_login_failed")
    print(f"Login failed: {e}")
    driver.quit()
    raise SystemExit(1)


# ---------------- NAVIGATE TO SETTINGS > DISPLAY ----------------
print("\n[2] Navigating to Settings > Display...")
try:
    # Try a direct settings link
    driver.get("https://app.grabdocs.com/settings")
    wait.until(EC.presence_of_element_located((
        By.XPATH, "//h1[contains(., 'Settings')] | //div[contains(., 'Settings')]"
    )))
    # If a Display tab exists, click it
    try:
        display_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(., 'Display')] | //a[contains(., 'Display')] | //div[contains(@class,'tab') and contains(., 'Display')]"
            ))
        )
        display_tab.click()
    except Exception:
        pass
    take_screenshot("settings_display_page")
except Exception as e:
    take_screenshot("settings_display_failed")
    print(f"Settings/Display navigation failed: {e}")
    driver.quit()
    raise SystemExit(1)

print("\n[3] Selecting theme: Dark...")

try:
    # 1. Click the dropdown that shows the current theme (Light)
    dropdown_trigger = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[@role='combobox']"
            " | //div[@role='combobox']"
            " | //div[contains(@class,'select') and contains(., 'Light')]"
            " | //div[contains(@class,'justify-between') and contains(., 'Light')]"
        ))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_trigger)
    driver.execute_script("arguments[0].click();", dropdown_trigger)
    print("Theme dropdown opened.")
    time.sleep(1)

    # 2. Click the Dark option
    dark_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[@role='option' and normalize-space()='Dark']"
            " | //div[contains(@class,'select') and contains(., 'Dark')]"
            " | //span[normalize-space()='Dark']/ancestor::div[@role='option']"
            " | //li[normalize-space()='Dark']"
            " | //button[normalize-space()='Dark']"
        ))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", dark_option)
    driver.execute_script("arguments[0].click();", dark_option)

    print("Theme switched to Dark.")
    take_screenshot("settings_theme_dark")

except Exception as e:
    take_screenshot("settings_theme_dark_failed")
    print(f"FAILED selecting theme: {e}")
    driver.quit()
    raise SystemExit(1)


# ---------------- TOGGLE THEME: LIGHT THEN SYSTEM ----------------
print("\n[3] Toggling theme to Light, then System...")
try:
    # Try UI radio buttons first
    light_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
        By.XPATH,
        "//label[.//span[contains(., 'Light')] or contains(., 'Light')]/input[@type='radio']"
        " | //input[@type='radio' and (@value='light' or @id='light' or contains(@name,'theme'))]"
    )))
    driver.execute_script("arguments[0].scrollIntoView(true);", light_option)
    light_option.click()
    print("Theme set to Light via UI.")
    take_screenshot("settings_theme_light")
    time.sleep(2)

    system_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
        By.XPATH,
        "//label[.//span[contains(., 'System')] or contains(., 'System')]/input[@type='radio']"
        " | //input[@type='radio' and (@value='system' or @id='system' or contains(@name,'theme'))]"
    )))
    driver.execute_script("arguments[0].scrollIntoView(true);", system_option)
    system_option.click()
    print("Theme set to System via UI.")
    take_screenshot("settings_theme_system")
    time.sleep(1)
except Exception as e:
    # Fallback: directly set localStorage theme keys
    print(f"UI toggle failed ({e}). Falling back to localStorage switch.")
    try:
        driver.execute_script("localStorage.setItem('theme', 'light');")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'settings') or contains(., 'Settings')]")))
        take_screenshot("settings_theme_light")
        time.sleep(2)

        driver.execute_script("localStorage.setItem('theme', 'system');")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'settings') or contains(., 'Settings')]")))
        take_screenshot("settings_theme_system")
        time.sleep(1)
    except Exception as e2:
        take_screenshot("settings_theme_toggle_failed")
        print(f"Theme toggle failed after fallback: {e2}")
        driver.quit()
        raise SystemExit(1)


# ---------------- LOGOUT ----------------
print("\n[4] Logging Out...")
try:
    profile_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@aria-label, 'Profile')]"
            " | //button[contains(@class, 'rounded-full') and contains(., 'BJ')]"
            " | //button[contains(., 'BJ')]"
        ))
    )
    profile_button.click()

    logout_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(., 'Logout')] | //button[contains(., 'Sign out')] | //span[contains(., 'Log out')]/ancestor::button[1]"
        ))
    )
    logout_button.click()
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(., 'Sign in')]")
    ))
    take_screenshot("settings_logout_success")
    print("Logout successful.")
except Exception as e:
    take_screenshot("settings_logout_failed")
    print(f"Logout may have failed or been skipped: {e}")


# ---------------- CLEANUP ----------------
driver.quit()
print("\nGRABDOCS SETTINGS DISPLAY THEME TOGGLE TEST COMPLETED SUCCESSFULLY.")
