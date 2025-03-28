from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# User details
CALENDLY_URL = "https://calendly.com/matejotys/30minutes?month=2025-04"
USER_NAME = "Radka Test"
USER_EMAIL = "radarudova@gmail.com"
UK_TIMEZONE = "UK"  # Adjust if needed
MEETING_TYPE = "Google Meet"
DATE = "1"  # Date to select
TIME = "16:00"  # Time to select

try:
    print("🔧 Setting up Chrome options...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # ← use new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    print("🚀 Starting WebDriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)

    print("🌐 Navigating to Calendly...")
    driver.get(CALENDLY_URL)

    ### STEP 1: Select Timezone ###
    print("🕐 Selecting timezone...")
    timezone_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "timezone-field")))
    timezone_dropdown.click()
    timezone_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#timezone-menu input")))
    timezone_input.send_keys("UK")
    time.sleep(2)

    timezone_options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[role='option']")))
    for option in timezone_options:
        if "UK, Ireland, Lisbon Time" in option.text:
            option.click()
            break
    time.sleep(2)

    ### STEP 2: Select Date ###
    print("📅 Selecting date...")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='calendar']")))
    date_select = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/button').click()
    time.sleep(4)

    ### STEP 3: Select Time Slot ###
    print("⏰ Looking for time slot...")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-container='time-button']")))
    available_times = driver.find_elements(By.CSS_SELECTOR, "button[data-container='time-button']")
    available_times_text = [t.text.strip() for t in available_times]
    print("Available times:", available_times_text)

    selected_time = None
    for time_slot in available_times:
        if time_slot.text.strip() == TIME:
            selected_time = time_slot
            break

    if not selected_time:
        print(f"❌ ERROR: Requested time {TIME} not found! Available options: {available_times_text}")
        driver.quit()
        exit()

    driver.execute_script("arguments[0].scrollIntoView();", selected_time)
    time.sleep(1)
    selected_time.click()
    print(f"✅ Selected time: {TIME}")

    ### STEP 4: Click "Next" ###
    print("➡️ Clicking 'Next' button...")
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Next')]")))
    next_button.click()

    ### STEP 5: Fill Details ###
    print("👤 Filling name and email...")
    name_field = wait.until(EC.presence_of_element_located((By.ID, "full_name_input")))
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email_input")))
    name_field.send_keys(USER_NAME)
    email_field.send_keys(USER_EMAIL)
    print(f"✅ Name & Email entered: {USER_NAME}, {USER_EMAIL}")

    ### STEP 6: Meeting Type ###
    print("📞 Selecting meeting location...")
    location_labels = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//label")))
    for label in location_labels:
        if MEETING_TYPE in label.text:
            driver.execute_script("arguments[0].scrollIntoView();", label)
            time.sleep(1)
            label.click()
            print(f"✅ Selected meeting type: {MEETING_TYPE}")
            break

    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()
    print("📨 Scheduled the event successfully!")

    time.sleep(5)
    driver.quit()

except Exception as e:
    print("❌ BOT CRASHED:")
    print(str(e))
    driver.quit()
    raise
