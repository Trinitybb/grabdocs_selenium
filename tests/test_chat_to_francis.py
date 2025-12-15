from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os, time

# ================= CONFIG =================
GRABDOCS_URL = "https://app.grabdocs.com/login"

EMAIL = "bowlingt0912@students.bowiestate.edu"
PASSWORD = "Testing123"
OTP_CODE = "335577"

SCREENSHOT_DIR = "screenshots_chat_history_francis"

# ================= SETUP =================
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

def take_screenshot(name):
    path = f"{SCREENSHOT_DIR}/{name}.png"
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 30)
actions = ActionChains(driver)

print("\n=== CHAT HISTORY → FRANCIS (REAL KEYBOARD INPUT) ===")

try:
    # ================= LOGIN =================
    driver.get(GRABDOCS_URL)

    email_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'Email') or @type='text']")
    ))
    email_input.send_keys(EMAIL)

    password_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']")
    ))
    password_input.send_keys(PASSWORD)

    sign_in_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Sign in') or contains(.,'Login')]")
    ))
    sign_in_btn.click()

    take_screenshot("login_submitted")

    # ================= OTP =================
    otp_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'OTP') or contains(@name,'otp')]")
    ))
    otp_input.send_keys(OTP_CODE)

    verify_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Verify') or contains(.,'Continue')]")
    ))
    verify_btn.click()

    take_screenshot("otp_verified")

    # ================= WAIT FOR CHAT HISTORY BUTTON =================
    history_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@title='Show History']")
    ))

    # ================= OPEN CHAT HISTORY =================
    history_button.click()
    time.sleep(0.5)
    take_screenshot("chat_history_opened")

    # ================= CLICK FRANCIS CHAT ROW =================
    francis_chat_row = wait.until(EC.element_to_be_clickable(
        (
            By.XPATH,
            "//h4[contains(text(),'Chat with GrabDocs Docs-Francis')]"
            "/ancestor::div[contains(@class,'flex')]"
        )
    ))

    francis_chat_row.click()
    time.sleep(0.5)
    take_screenshot("francis_chat_opened")

    # ================= SEND MESSAGE (REAL TYPING) =================
    chat_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[@contenteditable='true'] | //textarea")
    ))

    # CLICK INTO INPUT
    chat_input.click()
    time.sleep(0.2)

    message = "hello francis testing"

    # TYPE LIKE A HUMAN
    actions.move_to_element(chat_input).click().send_keys(message).send_keys(Keys.ENTER).perform()

    take_screenshot("message_typed_and_enter_pressed")
    print("Message typed and Enter pressed (ActionChains).")

    time.sleep(2)  # allow UI to process send

except Exception as e:
    take_screenshot("test_failed")
    print(f"TEST FAILED: {e}")

finally:
    driver.quit()
    print("\n=== TEST COMPLETE ===")
