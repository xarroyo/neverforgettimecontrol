import random
import time
from datetime import date, datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By

# driver_service = webdriver.FirefoxService(executable_path="/snap/bin/geckodriver")
# browser = webdriver.Firefox(service=driver_service)
# browser.implicitly_wait(10)

def login():
    browser.get("https://panel.intratime.es/weblogin/#/")
    user_field = browser.find_element(By.ID, "email").send_keys("user@email.com")
    pass_field = browser.find_element(By.ID, "pin-code").send_keys("####")
    access_button = browser.find_element(By.XPATH, "//button[@type='submit']").click()

def entrada():
    time.sleep(1)
    browser.find_element(By.XPATH, "//button/span/strong[text()='Entrada']").click()

def pausa():
    time.sleep(1)
    browser.find_element(By.XPATH, "//button/span/strong[text()='Pausa']").click()

def volver():
    time.sleep(1)
    browser.find_element(By.XPATH, "//button/span/strong[text()='Volver']").click()

def salida():
    time.sleep(1)
    browser.find_element(By.XPATH, "//button/span/strong[text()='Salida']").click()


def get_business_days(start, end):
    all_days = (start + timedelta(x + 1) for x in range((end - start).days))
    return [day for day in all_days if day.weekday() < 5]

def aprox_hour(base_time, marge_minuts=10):
    random_minutes = random.randint(-marge_minuts, marge_minuts)
    return base_time + timedelta(minutes=random_minutes)

def elapsed_time(hour1, hour2):
    td1 = timedelta(hours=hour1.hour, minutes=hour1.minute, seconds=hour1.second)
    td2 = timedelta(hours=hour2.hour, minutes=hour2.minute, seconds=hour2.second)
    return td1 - td2


def generar_horari(start_date, end_date):
    # Setup
    start_hour = datetime.strptime("09:00", "%H:%M")
    pause_hour = datetime.strptime("13:30", "%H:%M")
    return_hour = datetime.strptime("14:30", "%H:%M")
    finish_hour = datetime.strptime("18:00", "%H:%M")

    businness_days = get_business_days(start_date, end_date)
    total = timedelta()
    horaris = []
    for day in businness_days:
        aprox_start = aprox_hour(start_hour)
        aprox_pause = aprox_hour(pause_hour)
        aprox_return = aprox_hour(return_hour)
        aprox_finish = aprox_hour(finish_hour)
        hours = elapsed_time(aprox_pause, aprox_start) + elapsed_time(aprox_finish, aprox_return)

        total += hours
        horaris.append({
            "dia": day.strftime("%Y-%m-%d"),
            "entrada": aprox_start.strftime("%H:%M"),
            "pausa": aprox_pause.strftime("%H:%M"),
            "tornar": aprox_return.strftime("%H:%M"),
            "acabament": aprox_finish.strftime("%H:%M"),
            "hours": hours,
        })
    print(total.total_seconds()/3600 /4)
    return horaris

start_date = date(2022, 3, 1)
end_date = date(2022, 4, 1)
horaris = generar_horari(start_date, end_date)

for horari in horaris:
    print(f"Dia: {horari['dia']}, Entrada: {horari['entrada']}, Pausa: {horari['pausa']}, Tornar: {horari['tornar']}, Acabament: {horari['acabament']} => TOTAL: {horari['hours']}")