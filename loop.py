import time
from multiprocessing import Pool

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def open_ads_power_profile(profile_id):
    open_url = f"http://localhost:50325/api/v1/browser/start?user_id={profile_id}"
    close_url = f"http://localhost:50325/api/v1/browser/stop?user_id={profile_id}"
    response = requests.get(open_url)
    if response.ok:
        result = response.json()
        print(f'res: {result}')
        if result["code"] == 0:
            chrome_driver_path = result["data"]["webdriver"]
            debugger_address = result["data"]["ws"]["selenium"]
            return chrome_driver_path, debugger_address, close_url
        else:
            raise Exception(f"Помилка: {result['msg']}")
    else:
        raise Exception(f"HTTP помилка: {response.status_code}")


def setup_driver(chrome_driver_path, debugger_address):
    options = Options()
    options.add_experimental_option("debuggerAddress", debugger_address)
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def run_clicker(args):
    profile_id, max_click, min_click = args
    chrome_driver_path, debugger_address, close_url = open_ads_power_profile(profile_id)
    driver = setup_driver(chrome_driver_path, debugger_address)
    print('open')
    try:
        time.sleep(5)
        driver.get("https://orteil.dashnet.org/cookieclicker/")
        time.sleep(5)
        for i in range(1500):
            try:
                button = driver.find_element("xpath", "//button[@id='bigCookie']")
                button.click()
                time.sleep(0.03)
            except Exception:
                time.sleep(0.5)
                print(f"Нету в {profile_id}")
                continue
        print("Click off")
        time.sleep(10)
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        print('close')
        driver.quit()
        requests.get(close_url)


profile_ids = ["ksotjs2", "ksowkde"]


def run(max_click, min_click):
    params = [(profile_id, max_click, min_click) for profile_id in profile_ids]
    with Pool(len(profile_ids)) as pool:
        pool.map(run_clicker, params)


if __name__ == '__main__':
    run(max_click=5, min_click=5)
