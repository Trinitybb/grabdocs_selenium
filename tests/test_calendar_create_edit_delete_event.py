
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time, random

# ---- Random Realistic Title + Description ----
event_titles = [
    "Meeting", "Planning Session", "Client Project Discussion",
    "Operations Briefing", "Weekly Check-In",
    " Update", "Roadmap Review"
]

event_descriptions = [
    "Discuss priorities and progress for the upcoming week.",
    "Review key deliverables and adjust timelines.",
    "Coordinate project action items with the team.",
    "Plan work distribution and outline next phase tasks.",
    "Address outstanding issues and finalize decisions."
]

random_title = random.choice(event_titles)
random_description = random.choice(event_descriptions)
edited_title = random.choice(event_titles) + " UPDATED"


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


print("\n=== GRABDOCS CALENDAR TEST START ===")

# ---------------- LOGIN TEST ----------------
print("\n[1] Logging In...")

try:
    username_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='text' and not(contains(@placeholder, 'code'))]")
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
    take_screenshot("calendar_login_success")

    # ---- FIXED OTP STEP ----
    print("\nWaiting for OTP screen...")

    otp_field = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//input[contains(@placeholder, 'code') or contains(@placeholder, 'Code') or contains(@name, 'otp') or contains(@id, 'otp')]"
        ))
    )

    time.sleep(0.5)  # small buffer for UI animation

    otp_field.send_keys("335577")
    print("OTP entered correctly (NOT in username box).")

    verify_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(., 'Verify')] | //button[contains(., 'Continue')] | //button[contains(., 'Submit')]"
        ))
    )
    verify_button.click()
    take_screenshot("calendar_otp_verified")

    # ---- Wait for dashboard ----
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((
            By.XPATH, "//div[contains(., 'Drop files') or contains(., 'Workspace')]"
        ))
    )
    take_screenshot("calendar_dashboard_loaded")

except Exception as e:
    take_screenshot("calendar_login_failed")
    print(f"Login failed: {e}")


# ---------------- GO TO CALENDAR ----------------
print("\n[2] Navigating to Calendar...")

calendar_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//a[contains(., 'Calendar')]")
))
calendar_button.click()
time.sleep(2)
take_screenshot("calendar_page_loaded")

# Directly open the create page to avoid missing the button click
driver.get("https://app.grabdocs.com/calendar/create")
create_form_loaded = wait.until(EC.presence_of_element_located((
    By.XPATH, "//h1[contains(., 'Create New Event')]"
)))
take_screenshot("calendar_create_event_screen")


# ---------------- CREATE EVENT ----------------
print("\n[3] Creating New Event...")

try:
    # TITLE FIELD (exact placeholder from UI)
    title_box = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//input[@placeholder='Team Meeting, Client Call, etc.']"
    )))
    title_box.clear()
    title_box.send_keys(random_title)

    # DESCRIPTION FIELD (exact placeholder)
    desc_box = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//textarea[@placeholder='Add details about the event...']"
    )))
    desc_box.clear()
    desc_box.send_keys(random_description)

    # SET START DATE/TIME (use label relationships to avoid index issues)
    start_date = wait.until(EC.presence_of_element_located((
        By.XPATH, "//label[contains(., 'Start Date')]/following::input[@type='date'][1]"
    )))
    start_date.clear()
    start_date.send_keys("11/20/2025")

    start_time = wait.until(EC.presence_of_element_located((
        By.XPATH, "//label[contains(., 'Start Date')]/following::input[@type='time'][1]"
    )))
    start_time.clear()
    start_time.send_keys("09:00")

    # SET END DATE/TIME
    end_date = wait.until(EC.presence_of_element_located((
        By.XPATH, "//label[contains(., 'End Date')]/following::input[@type='date'][1]"
    )))
    end_date.clear()
    end_date.send_keys("11/20/2025")

    end_time = wait.until(EC.presence_of_element_located((
        By.XPATH, "//label[contains(., 'End Date')]/following::input[@type='time'][1]"
    )))
    end_time.clear()
    end_time.send_keys("06:00 PM")

    take_screenshot("calendar_event_filled")

    # CLICK CREATE EVENT
    save_event = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='Create Event'] | //button[contains(., 'Create Event')]")
    ))
    save_event.click()
    time.sleep(3)

    print("Event Created Successfully.")
    take_screenshot("calendar_event_created")

except Exception as e:
    take_screenshot("calendar_event_create_failed")
    print(f"Event creation failed: {e}")
    driver.quit()
    exit()


# ---------------- OPEN NEWLY CREATED EVENT ----------------
print("\n[4] Opening Event...")

# Go back to calendar view and click the event tile in the grid
driver.get("https://app.grabdocs.com/calendar")
wait.until(EC.presence_of_element_located((
    By.XPATH, "//div[contains(@class,'rbc-calendar')]"
)))
event_tile = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    f"//div[contains(@class,'rbc-event-content')]//div[contains(., '{random_title}')]"
))
)
event_tile.click()
take_screenshot("calendar_event_opened")

# Wait for event detail page to render (shows the title)
wait.until(EC.presence_of_element_located((
    By.XPATH, f"//h1[contains(., '{random_title}')]"
)))


# ---------------- DELETE EVENT ----------------
print("\n[5] Deleting Event...")

delete_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH,
     "(//div[contains(@class,'space-x-2')]/button[contains(@class,'border-red')])[1]"
     " | //button[contains(@aria-label, 'Delete')]"
     " | //button[normalize-space()='Delete']"
     " | //span[contains(., 'Delete')]/ancestor::button[1]"
     )
))
delete_btn.click()

confirm_delete = wait.until(EC.element_to_be_clickable(
    (By.XPATH,
     "//button[contains(., 'Delete')]"
     " | //span[contains(., 'Delete')]/ancestor::button[1]"
     )
))
confirm_delete.click()

take_screenshot("calendar_event_deleted")

print("\nEvent successfully created and deleted.")


# ---------------- LOGOUT ----------------
print("\n[6] Logging Out...")
try:
    # Open profile menu if present
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
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Sign in')]")))
    take_screenshot("calendar_logout_success")
    print("Logout successful.")
except Exception as e:
    take_screenshot("calendar_logout_failed")
    print(f"Logout may have failed or been skipped: {e}")


# ---------------- CLEANUP ----------------
driver.quit()
print("\nGRABDOCS CALENDAR TEST COMPLETED SUCCESSFULLY.")
