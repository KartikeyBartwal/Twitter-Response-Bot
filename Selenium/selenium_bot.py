from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Initialize the webdriver (e.g. Chrome)
driver = webdriver.Chrome()

# Navigate to Twitter
driver.get("https://twitter.com")

# Wait for the user to log in
input("Press Enter after logging in to Twitter...")

# Start scrolling down slowly
while True:

    # SCROLL DOWN SLOWLY
    driver.execute_script("window.scrollBy(0, 100);")

    # SLEEP FOR 1 SECOND
    time.sleep(1)

    # CHECK IF 10 SECONDS HAVE PASSED
    if int(time.time()) % 10 == 0:

        # TAKE A SCREENSHOT
        driver.save_screenshot(f"screenshot_{int(time.time())}.png")

