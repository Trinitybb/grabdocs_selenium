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

# ---------- SLOW MODE ----------
SLOW_MODE = True
SLOW_DELAY = 0.8

def slow():
    if SLOW_MODE:
        time.sleep(SLOW_DELAY)

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

wait = WebDriverWait(driver, 40)
actions = ActionChains(driver)

print("\n=== CHAT HISTORY → FRANCIS ONODUEZE I (REAL CLICK) ===")

try:
    # ================= LOGIN =================
    driver.get(GRABDOCS_URL)
    slow()

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'Email') or @type='text']")
    )).send_keys(EMAIL)
    slow()

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']")
    )).send_keys(PASSWORD)
    slow()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Sign in') or contains(.,'Login')]")
    )).click()
    slow()

    take_screenshot("login_submitted")

    # ================= OTP =================
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'OTP') or contains(@name,'otp')]")
    )).send_keys(OTP_CODE)
    slow()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Verify') or contains(.,'Continue')]")
    )).click()
    slow()

    take_screenshot("otp_verified")

    # ================= OPEN CHAT HISTORY =================
    history_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@title='Show History']")
    ))
    history_button.click()
    slow()

    take_screenshot("chat_history_opened")

    # ================= CLICK FRANCIS (CORRECT WAY) =================
    print("Selecting Francis Onodueze I chat...")
    slow()

    francis_h4 = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//h4[normalize-space()='Chat with Francis Onodueze I']")
    ))

    # Scroll into view
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        francis_h4
    )
    slow()

    # REAL mouse click on the <h4>
    actions.move_to_element(francis_h4) \
           .pause(0.3) \
           .click() \
           .perform()

    slow()
    take_screenshot("francis_chat_selected")
    print("Francis chat selected.")

    # ================= SEND MESSAGE =================
    print("Typing message to Francis...")
    slow()

    chat_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[@contenteditable='true'] | //textarea")
    ))

    actions.move_to_element(chat_input).click().perform()
    slow()

    message = "hello francis testing"

    for char in message:
        actions.send_keys(char).pause(0.08)
    actions.send_keys(Keys.ENTER).perform()

    slow()
    take_screenshot("message_sent")
    print("Message sent to Francis.")

except Exception as e:
    take_screenshot("test_failed")
    print(f"❌ TEST FAILED: {e}")

finally:
    driver.quit()
    print("\n=== TEST COMPLETE ===")
