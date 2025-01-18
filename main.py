import datetime
import json
import random
import threading
import time
import tkinter as tk

import requests
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium_stealth import stealth

is_enabled = True
initial_x, initial_y = 0, 0

APP_TITLE = "Автоклікер"
current_thread = None
is_procecing = False
counter = 0
profile_ids = ["ksotjs2", "ksowkde"]
profile_ids1 = ["kspg9f5", "kspg9am"]
profile_ids3 = ["j63rj35", "j64qwa1", "j65ft68", "j65hpjg", "j65ipt3"]
counter_lock = threading.Lock()
URL = 'https://orteil.dashnet.org/cookieclicker/'
URL1 = 'https://tap.eclipse.xyz/'
element_xpath1 = '//button[@id="bigCookie"]'
element_xpath2 = '//canvas[@data-sentry-element="Stage"]'
X1, Y1 = 150, 300
X2, Y2 = 700, 300
with open("profile.txt", "r") as f:
    profiles = f.read().split("\n")
profile_ids4 = profiles
print(f"pr: {profile_ids4}")


def open_ads_power_profile(profile_id):
    open_url = f"http://localhost:50325/api/v1/browser/start?user_id={profile_id}"
    close_url = f"http://localhost:50325/api/v1/browser/stop?user_id={profile_id}"
    response = requests.get(open_url)
    if response.ok:
        result = response.json()
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


def run_clicker(profile_id, max_click, min_click, sleep_chance, min_sleep, max_sleep, slow_chance, slow_strength,
                min_deeply_sleep, max_deeply_sleep, min_simple_state,
                max_simple_state):
    global counter, is_procecing, current_thread
    try:
        chrome_driver_path, debugger_address, close_url = open_ads_power_profile(profile_id)
        driver = setup_driver(chrome_driver_path, debugger_address)
    except Exception as e:
        console_label.config(text=f'Сталась помилка {str(e)}. \n Мабуть Ads power не запущений.', fg="red")
        is_procecing = False
        current_thread = None
        run_button.config(state=tk.NORMAL, text="Запустити")
        entry1.config(state=tk.NORMAL)
        entry2.config(state=tk.NORMAL)
        entry3.config(state=tk.NORMAL)
        entry4.config(state=tk.NORMAL)
        entry5.config(state=tk.NORMAL)
        entry6.config(state=tk.NORMAL)
        entry7.config(state=tk.NORMAL)
        reset_button.config(state=tk.NORMAL)
        return
    try:
        print("Open")
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        print("Hide driver,,,,")
        if not is_procecing:
            raise AssertionError
        driver.get(URL1)
        if not is_procecing:
            raise AssertionError
        time.sleep(2)
        if not is_procecing:
            raise AssertionError
        time.sleep(2)
        with counter_lock:
            counter += 1
            print(Fore.RED + f"Counter updated to {counter}" + Style.RESET_ALL)
            if counter >= len(profile_ids1):
                run_button.config(state=tk.NORMAL)
                console_label.config(text='Успішно приєднано! Починаю клікання', fg="green")
        is_slow = False
        # x, y = X1 + random.randint(-10, 10), Y1 + random.randint(-10, 10)  # x = 700 y = 300
        # element = driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]);", x, y)
        element = driver.find_element("xpath", element_xpath2)
        print(f'element: {str(element)}')
        need_to_take = False
        offset_x, offset_y = 0, 0
        sleep_data = datetime.datetime.now() + datetime.timedelta(
            minutes=round(random.uniform(min_simple_state, max_simple_state), 3))
        while is_procecing:
            if datetime.datetime.now() > sleep_data:
                deply_sleep = random.randrange(int(min_deeply_sleep * 60), int(max_deeply_sleep * 60))
                b = 0
                while b <= deply_sleep:
                    time.sleep(1)
                    b += 1
                    if not is_procecing:
                        return
                sleep_data = datetime.datetime.now() + datetime.timedelta(
                    minutes=round(random.uniform(min_simple_state, max_simple_state), 3))
            if random.randrange(0, 400) == 0 or need_to_take:
                need_to_take = False
                # x, y = 150 + random.randint(-10, 10), 300 + random.randint(-10, 10)
                element = driver.find_element("xpath", element_xpath2)
            if random.randrange(0, 50) == 5:
                offset_x, offset_y = random.randint(-5, 5), random.randint(-5, 5)
            if not isinstance(element, WebElement):
                time.sleep(0.1)
                print('not')
                need_to_take = True
                continue
            try:
                if random.randrange(0, 10) == 0:
                    actions = ActionChains(driver)
                    print(f"offset x: {offset_x}, offset y: {offset_y}")
                    actions.move_to_element_with_offset(element, offset_x, offset_y).click().perform()
                    print('norm 0')
                else:
                    element.click()
                    print('norm 1')
            except Exception:
                time.sleep(0.1)
                print('not1')
                need_to_take = True
                continue
            if random.randrange(0, int(100 / slow_chance)) == 0:
                is_slow = True
            if random.randrange(0, 50) == 0:
                is_slow = False
            s_str = 1 / max(0.01, slow_strength)
            time.sleep(
                round(random.uniform(max(0.01, float(min_click)), max(0.02, max_click)) * (s_str if is_slow else 1), 5))
            if random.randrange(0, int((100 / sleep_chance))) == 0:
                time.sleep(random.uniform(min_sleep, max_sleep))
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        print("Close")
        driver.quit()
        requests.get(close_url)


def run(max_click, min_click, sleep_chance, min_sleep, max_sleep, slow_chance, slow_strength, min_deeply_sleep,
        max_deeply_sleep, min_simple_state,
        max_simple_state):
    threads = []
    global is_procecing, current_thread
    for profile_id in profile_ids1:
        thread = threading.Thread(target=run_clicker,
                                  args=(
                                      profile_id, max_click, min_click, sleep_chance, min_sleep, max_sleep, slow_chance,
                                      slow_strength, min_deeply_sleep, max_deeply_sleep, min_simple_state,
                                      max_simple_state),
                                  daemon=True)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print('End!')


def toggle_run():
    global current_thread, is_procecing, counter
    if run_button.config('text')[-1] == "Запустити":
        if (current_thread is None) or (current_thread is not None and not current_thread.is_alive()):
            max_click = float(entry1.get())
            min_click = float(entry2.get())
            sleep_chance = float(entry3.get())
            min_sleep = float(entry4.get())
            max_sleep = float(entry5.get())
            slow_chance = float(entry6.get())
            slow_strength = float(entry7.get())
            min_deeply_sleep = float(entry8.get())
            max_deeply_sleep = float(entry9.get())
            min_simple_state = float(entry10.get())
            max_simple_state = float(entry11.get())
            entry1.config(state=tk.DISABLED)
            entry2.config(state=tk.DISABLED)
            entry3.config(state=tk.DISABLED)
            entry4.config(state=tk.DISABLED)
            entry5.config(state=tk.DISABLED)
            entry6.config(state=tk.DISABLED)
            entry7.config(state=tk.DISABLED)
            entry8.config(state=tk.DISABLED)
            entry9.config(state=tk.DISABLED)
            entry10.config(state=tk.DISABLED)
            entry11.config(state=tk.DISABLED)
            reset_button.config(state=tk.DISABLED)
            run_button.config(text="Отменить")
            run_button.config(state=tk.DISABLED)
            is_procecing = True
            print(f"[DEBUG] is_procecing set to {is_procecing}")
            console_label.config(text='⚠ Приєднуюся до браузерів. Зачекайте!!!', fg="red")
            counter = 0
            current_thread = threading.Thread(target=run,
                                              args=(
                                                  max_click, min_click, sleep_chance, min_sleep, max_sleep, slow_chance,
                                                  slow_strength, min_deeply_sleep, max_deeply_sleep, min_simple_state,
                                                  max_simple_state,),
                                              daemon=True)
            current_thread.start()
        else:
            warn = f"Потік {current_thread.name if current_thread else 'None'} ще не завершено!"
            print(warn)
            console_label.config(text=warn, fg="red")
    else:
        is_procecing = False
        console_label.config(text="Зачекайте 5-15 секунд завершуємо всі процеси! Не клацайте нікуди!")
        print(f"[DEBUG] is_procecing set to {is_procecing}")
        print('OK')
        current_thread.join() if current_thread else None
        current_thread = None
        entry1.config(state=tk.NORMAL)
        entry2.config(state=tk.NORMAL)
        entry3.config(state=tk.NORMAL)
        entry4.config(state=tk.NORMAL)
        entry5.config(state=tk.NORMAL)
        entry6.config(state=tk.NORMAL)
        entry7.config(state=tk.NORMAL)
        entry8.config(state=tk.NORMAL)
        entry9.config(state=tk.NORMAL)
        entry10.config(state=tk.NORMAL)
        entry11.config(state=tk.NORMAL)
        reset_button.config(state=tk.NORMAL)
        run_button.config(text="Запустити")
        console_label.config(
            text='Успішно скасовано! Натисніть запустити, щоб підключитися до браузерів і почати автоклікання',
            fg="green")


def enforce_range(entry_widget, min_value=0, max_value=1):
    try:
        value = entry_widget.get().lstrip("0") or "0"
        value = float(value)
        if value < min_value:
            value = min_value
        elif value > max_value:
            value = max_value
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, str(value))
    except ValueError:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, str(min_value))


def validate_input(new_value):
    if new_value == "" or new_value == ".":
        return True
    try:
        value = float(new_value)
        return 0 <= value <= 1
    except ValueError:
        return False


def validate_input1(new_value):
    if new_value == "" or new_value == ".":
        return True
    try:
        value = float(new_value)
        return 2 <= value <= 60
    except ValueError:
        return False


def validate_input2(new_value):
    if new_value == "" or new_value == ".":
        return True
    try:
        value = float(new_value)
        return 4 <= value <= 120
    except ValueError:
        return False


def reset_defaults():
    if is_enabled:
        entry1.delete(0, tk.END)
        entry1.insert(0, "0.07")
        entry2.delete(0, tk.END)
        entry2.insert(0, "0.3")
        entry3.delete(0, tk.END)
        entry3.insert(0, "0.1")
        entry4.delete(0, tk.END)
        entry4.insert(0, "5.0")
        entry5.delete(0, tk.END)
        entry5.insert(0, "15.0")
        entry6.delete(0, tk.END)
        entry6.insert(0, "0.1")
        entry7.delete(0, tk.END)
        entry7.insert(0, "0.6")
        entry8.delete(0, tk.END)
        entry8.insert(0, "15.0")
        entry9.delete(0, tk.END)
        entry9.insert(0, "25.0")
        entry10.delete(0, tk.END)
        entry10.insert(0, "25.0")
        entry11.delete(0, tk.END)
        entry11.insert(0, "40.0")


def main():
    global entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entry10, entry11, console_label, reset_button, run_button, console_label
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("1080x920")
    tk.Label(root, text=APP_TITLE, font=("Arial", 14, "bold"), fg="blue").pack(pady=10)
    tk.Label(root, text="⚠ Усі значення налаштовані для мінімізації ризику бана", fg="red").pack(pady=10)
    tk.Label(root, text="⚠ Рекомендуємо не зміняти значеня!", fg="red").pack(pady=10)
    tk.Label(root, text="⚠ Обов'язково включіть Ads Power!", fg="red").pack(pady=10)
    validate_cmd = root.register(validate_input)
    validate_cmd1 = root.register(validate_input1)
    validate_cmd2 = root.register(validate_input2)
    tk.Label(root, text="Інтервал між кліками (секунди):", anchor="w").pack(pady=2)
    entry1 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry1.insert(0, "0.07")
    entry1.pack(pady=2)
    entry1.bind("<FocusOut>", lambda event: enforce_range(entry1))
    tk.Label(root, text="Максимальний інтервал між кліками (секунди):", anchor="w").pack(pady=2)
    entry2 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry2.insert(0, "0.3")
    entry2.pack(pady=2)
    entry2.bind("<FocusOut>", lambda event: enforce_range(entry2))
    tk.Label(root, text="Шанс короткого засинання 1.0 це 1% після кліку", anchor="w").pack(pady=2)
    entry3 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry3.insert(0, "0.1")
    entry3.pack(pady=2)
    entry3.bind("<FocusOut>", lambda event: enforce_range(entry3))
    tk.Label(root, text="Мінімальний відрізок короткого сну (секунди): ", anchor="w").pack(pady=2)
    entry4 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd1, '%P'))
    entry4.insert(0, "5.0")
    entry4.pack(pady=2)
    entry4.bind("<FocusOut>", lambda event: enforce_range(entry4, 2, 60))
    tk.Label(root, text="Максимальний відрізок короткого сну (секунди):", anchor="w").pack(pady=2)
    entry5 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd2, '%P'))
    entry5.insert(0, "15.0")
    entry5.pack(pady=2)
    entry5.bind("<FocusOut>", lambda event: enforce_range(entry5, 4, 120))
    tk.Label(root, text="Шанс на тимчасовий повільньний режим:", anchor="w").pack(pady=2)
    entry6 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry6.insert(0, "0.1")
    entry6.pack(pady=2)
    entry6.bind("<FocusOut>", lambda event: enforce_range(entry6))
    tk.Label(root, text="Повільність повільного режима:", anchor="w").pack(pady=2)
    entry7 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry7.insert(0, "0.6")
    entry7.pack(pady=2)
    entry7.bind("<FocusOut>", lambda event: enforce_range(entry7))
    tk.Label(root, text="Мінімальна тривалість глибокого сну (хвилини):", anchor="w").pack(pady=2)
    entry8 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd2, '%P'))
    entry8.insert(0, "15.0")
    entry8.pack(pady=2)
    entry8.bind("<FocusOut>", lambda event: enforce_range(entry8, 4, 120))
    tk.Label(root, text="Максимальна тривалість глибокого сну (хвилини):", anchor="w").pack(pady=2)
    entry9 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd2, '%P'))
    entry9.insert(0, "25.0")
    entry9.pack(pady=2)
    entry9.bind("<FocusOut>", lambda event: enforce_range(entry9, 4, 120))
    tk.Label(root, text="Мінімальна тривалість звичайного режиму перед глибоким сном (хвилини): ", anchor="w").pack(pady=2)
    entry10 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd2, '%P'))
    entry10.insert(0, "25.0")
    entry10.pack(pady=2)
    entry10.bind("<FocusOut>", lambda event: enforce_range(entry10, 4, 120))
    tk.Label(root, text="Максимальна тривалість звичайного режиму перед глибоким сном (хвилини): ", anchor="w").pack(pady=2)
    entry11 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd2, '%P'))
    entry11.insert(0, "40.0")
    entry11.pack(pady=2)
    entry11.bind("<FocusOut>", lambda event: enforce_range(entry11, 4, 120))
    reset_button = tk.Button(root, text="Скинути параметри", command=reset_defaults)
    reset_button.pack(pady=10)
    run_button = tk.Button(root, text="Запустити", command=toggle_run)
    run_button.pack(pady=10)
    console_label = tk.Label(root, text="", fg="green")
    console_label.pack(pady=10)
    console_label.config(text="Натисніть запустити, щоб підключитися до браузерів і почати автоклікання")
    root.mainloop()


if __name__ == '__main__':
    main()
