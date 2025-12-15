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

EMAIL = os.getenv("GRABDOCS_EMAIL", "bowlingt0912@students.bowiestate.edu")
PASSWORD = os.getenv("GRABDOCS_PASSWORD", "Testing123")
OTP_CODE = os.getenv("GRABDOCS_OTP", "335577")

SCREENSHOT_DIR = "screenshots_housekeeping_absolute"

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

print("\n=== CHAT HISTORY → #HOUSE KEEPING (ABSOLUTE XPATH) ===")

try:
    # ================= LOGIN =================
    driver.get(GRABDOCS_URL)

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'Email') or @type='text']")
    )).send_keys(EMAIL)

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']")
    )).send_keys(PASSWORD)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Sign in') or contains(.,'Login')]")
    )).click()

    take_screenshot("login_submitted")

    # ================= OTP =================
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'OTP') or contains(@name,'otp')]")
    )).send_keys(OTP_CODE)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Verify') or contains(.,'Continue')]")
    )).click()

    take_screenshot("otp_verified")

    # ================= OPEN CHAT HISTORY =================
    history_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@title='Show History']")
    ))
    history_button.click()
    time.sleep(0.7)
    take_screenshot("chat_history_opened")

    # ================= CLICK EXACT HOUSEKEEPING ROW =================
    print("Clicking EXACT #house keeping row (absolute XPath)...")

    housekeeping_row = wait.until(EC.element_to_be_clickable(
        (
            By.XPATH,
            "/html/body/div/div[1]/main/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div"
        )
    ))

    driver.execute_script("arguments[0].scrollIntoView(true);", housekeeping_row)
    time.sleep(0.3)
    housekeeping_row.click()

    take_screenshot("housekeeping_chat_opened")

    # ================= TYPE MESSAGE =================
    print("Typing message into #house keeping...")

    chat_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[@contenteditable='true'] | //textarea")
    ))

    chat_input.click()
    time.sleep(0.2)

    message = "hello from selenium testing 12/14/2025 -Trinity Bowling"

    actions.move_to_element(chat_input) \
           .click() \
           .send_keys(message) \
           .send_keys(Keys.ENTER) \
           .perform()

    take_screenshot("housekeeping_message_sent")
    print("Message typed and Enter pressed.")

    time.sleep(2)

except Exception as e:
    take_screenshot("test_failed")
    print(f"❌ TEST FAILED: {e}")

finally:
    driver.quit()
    print("\n=== TEST COMPLETE ===")
