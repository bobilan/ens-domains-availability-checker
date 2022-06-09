import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from art import tprint


def check_availability(file_name):
    availability = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/div[2]/a[1]/div[1]/div[1]")))
    if availability.text == "Available":
        with open(f"{file_name}", "a") as f:
            return f.write(f"\n{input_value} - Available")


def check_expiry_date(expiry_input, file_name):
    expiry_date = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/div[2]/a[1]/p[1]")))
    if f"{expiry_input}" in expiry_date.text:
        with open(f"{file_name}", "a") as f:
            return f.write(f"\n{input_value} - {expiry_date.text}")


def reserve_list():
    with open("reserve_list.txt", "w") as f:
        f.write(str(count))


def get_from_reserve():
    global reserve_start
    with open("reserve_list.txt", "r") as f:
        reserve_start = int(f.read())
        return reserve_start


def get_start_page(input_url):
    driver.get(f"{input_url}")


def main(file_name, start_number):
    tprint("Let's  find  domains", font="big")
    print("Searching...")
    search = WebDriverWait(driver, 60).until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/div[1]/header[1]/form[1]/input[1]")))
    global input_value
    global count
    with open(f"{file_name}", "r") as names:
        for count, input_value in enumerate(names):
            if count >= start_number:
                reserve_list()
                actions.click(search).perform()
                actions.send_keys(input_value).perform()
                time.sleep(3)

                actions.send_keys(Keys.ENTER)
                actions.perform()

                if check_availability(save_to):
                    continue
                elif check_expiry_date("2022.06", save_to):  # Date range
                    continue
                elif check_expiry_date("2022.07", save_to):  # Date range
                    continue
                # time.sleep(1)


s = Service('/Users/Bo/Desktop/Files/Coding/selenium/chromedriver2')
driver = webdriver.Chrome(service=s)
actions = ActionChains(driver)
input_value = None
count = None
reserve_start = None
save_to = "domains.txt"  # Specify the file to save the results to

get_start_page("https://app.ens.domains/search/000")
time.sleep(10)

try:
    main("input_data.txt", 24908)  # Specify file to get inputs from, and line number for START VALUE in that file

except TimeoutException:
    print("TimeoutException")
    get_from_reserve()
    time.sleep(2)
    main("input_data.txt", reserve_start)

except StaleElementReferenceException:
    print("StaleElementReferenceException")
    get_from_reserve()
    time.sleep(2)
    main("input_data.txt", reserve_start)

except WebDriverException:
    print("WebDriverException")
    s = Service('/Users/Bo/Desktop/Files/Coding/selenium/chromedriver2')
    driver = webdriver.Chrome(service=s)
    actions = ActionChains(driver)
    input_value = None
    count = None
    reserve_start = None
    save_to = "domains.txt"  # Specify the file to save the results to

    get_start_page("https://app.ens.domains/search/000")
    timeout = 5

    get_from_reserve()
    time.sleep(2)
    main("input_data.txt", reserve_start)

finally:
    get_from_reserve()
    time.sleep(2)
    main("input_data.txt", reserve_start)

print("Last try...")
main("input_data.txt", reserve_start)

print(f"Here we stopped: {reserve_start}")


time.sleep(5)
driver.quit()


