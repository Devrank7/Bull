import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium_stealth import stealth

options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
driver.get("https://bot.sannysoft.com/")
time.sleep(20)
