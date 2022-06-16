import chromedriver_autoinstaller
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from art import tprint

EXCEPTION_MSG = "Exception occurred [{}]"
EXECUTABLE_PATH = "https://app.ens.domains/search/000"

chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')


class DomainChecker:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.actions = ActionChains(self.driver)
        self.input_value = ""
        self.count = None
        self.reserve_start = 0
        self.save_to = "domains.txt"
        self.get_from = "input_data.txt"

    def check_availability(self):
        availability = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/div[2]/a[1]/div[1]/div[1]")
            )
        )
        if availability.text == "Available":
            with open(f"{self.save_to}", "a") as f:
                return f.write(f"\n{self.input_value} - Available")

    def check_expiry_date(self, expiry_input):
        expiry_date = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/div[2]/a[1]/p[1]")))
        if f"{expiry_input}" in expiry_date.text:
            with open(f"{self.save_to}", "a") as f:
                return f.write(f"\n{self.input_value} - {expiry_date.text}")  # how to get input value from iteration
    # here

    def reserve_list(self):
        with open("reserve_list.txt", "w") as f:
            f.write(str(self.count))

    def get_from_reserve(self):
        with open("reserve_list.txt", "r") as f:
            self.reserve_start = int(f.read())

    def get_start_page(self):
        self.driver.get(f"{EXECUTABLE_PATH}")

    def main(self, start_number):
        tprint("Let's  find  domains", font="big")
        print("Searching...")
        search = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "/html[1]/body[1]/div[1]/header[1]/form[1]/input[1]")))
        with open(f"{self.get_from}", "r") as names:
            for count, self.input_value in enumerate(names):
                if count >= start_number:
                    self.reserve_list()
                    self.actions.click(search).perform()
                    self.actions.send_keys(self.input_value).perform()
                    time.sleep(3)

                    self.actions.send_keys(Keys.ENTER)
                    self.actions.perform()

                    if self.check_availability():
                        continue
                    elif self.check_expiry_date("2022.06"):  # Date range
                        continue
                    elif self.check_expiry_date("2022.07"):  # Date range
                        continue


domain_checker = DomainChecker()

domain_checker.get_start_page()
time.sleep(10)

try:
    domain_checker.main(1)  # SPECIFY START VALUE NUMBER

except TimeoutException as e:
    print(EXCEPTION_MSG.format(e))
    domain_checker.get_from_reserve()
    time.sleep(2)
    domain_checker.main(domain_checker.reserve_start)  # how to get to class variable???

except StaleElementReferenceException as e:
    print(EXCEPTION_MSG.format(e))
    domain_checker.get_from_reserve()
    time.sleep(2)
    domain_checker.main(domain_checker.reserve_start)

except WebDriverException as e:
    domain_checker.get_start_page()
    time.sleep(10)
    domain_checker.get_from_reserve()
    domain_checker.main(domain_checker.reserve_start)

finally:
    domain_checker.get_from_reserve()
    domain_checker.main(domain_checker.reserve_start)

print("Last try...")
domain_checker.get_from_reserve()
domain_checker.main(domain_checker.reserve_start)
print(f"Here we stopped: {domain_checker.reserve_start}")

time.sleep(5)
domain_checker.driver.quit()