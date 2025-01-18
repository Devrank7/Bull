import time

from selenium.webdriver import Chrome, ChromeOptions


# from selenium_stealth import stealth
#
# options = ChromeOptions()
# # options.add_experimental_option("excludeSwitches", ["enable-automation"])
# # options.add_experimental_option("useAutomationExtension", False)
# # options.add_argument('--disable-blink-features=AutomationControlled')
# driver = Chrome(options=options)
# # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# # stealth(driver,
# #         languages=["en-US", "en"],
# #         vendor="Google Inc.",
# #         platform="Win32",
# #         webgl_vendor="Intel Inc.",
# #         renderer="Intel Iris OpenGL Engine",
# #         fix_hairline=True,
# #         )
# driver.get("https://bot.sannysoft.com/")
# properties = driver.execute_script('return Object.keys(window);')
# cdc_properties = [prop for prop in properties if prop.startswith('cdc_')]
# if cdc_properties:
#     print(f" 1 Знайдено властивості, що починаються з 'cdc_': {cdc_properties}")
# else:
#     print(" 1 Властивості, що починаються з 'cdc_', не знайдено.")
# time.sleep(20)
def main():
    try:
        i = 0
        print('lll')
        if i == 0:
            return
    finally:
        print('has')

if __name__ == '__main__':
    main()