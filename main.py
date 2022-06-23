import time
import re
import datetime
from dateutil.relativedelta import relativedelta
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from art import tprint
from telegram_notification_bot import send_message_to_channel
from ens_domain_database import (
    get_from_input_data,
    insert_available,
    insert_expires_soon,
    update_reserve_list,
    get_from_reserve_list,
)


EXCEPTION_MSG = "Exception occurred [{}]"
EXECUTABLE_PATH = "https://app.ens.domains/search/000"
GRACE_PERIOD = "grace period ends"
EXPIRY_PERIOD = "expires"
AVAILABLE_STATUS = "available"

chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")


class DomainChecker:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.actions = ActionChains(self.driver)
        self.input_value = ""
        self.count = 0
        self.reserve_start = get_from_reserve_list()
        self.names = get_from_input_data()

    def check_availability(self):
        availability = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html[1]/body[1]/div[1]/div[1]/main[1]/div[2]/a[1]/div[1]/div[1]",
                )
            )
        )
        if availability.text.lower() == AVAILABLE_STATUS:
            send_message_to_channel(
                f"🎉 This domain might be Available: https://app.ens.domains/search/{self.input_value}"
            )
            insert_available(self.input_value, AVAILABLE_STATUS)

    @staticmethod
    def regex_get_date_(self, text):
        match = re.findall(r"\d\d\d\d\.\d\d.\d\d", text)
        return match[0]

    @staticmethod
    def current_month():
        date = datetime.datetime.today()
        return date.strftime("%Y.%m")

    @staticmethod
    def next_month(number_of_months):
        following_month = datetime.datetime.today() + relativedelta(months=number_of_months)
        return following_month.strftime("%Y.%m")

    def check_expiry_date(self, expiry_input):
        expiry_date = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/div[2]/a[1]/p[1]")
            )
        )
        if f"{expiry_input}" in expiry_date.text:
            regex_date = self.regex_get_date_(expiry_date.text)
            if EXPIRY_PERIOD in expiry_date.text.lower():
                insert_expires_soon(self.input_value, EXPIRY_PERIOD, regex_date)
            if GRACE_PERIOD in expiry_date.text.lower():
                insert_expires_soon(self.input_value, GRACE_PERIOD, regex_date)

    def reserve_list(self):
        return update_reserve_list(self.count)

    def get_start_page(self):
        self.driver.get(f"{EXECUTABLE_PATH}")

    def main(self, start_number):
        tprint("Let's  find  domains", font="big")
        print("Searching...")
        search = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html[1]/body[1]/div[1]/header[1]/form[1]/input[1]")
            )
        )
        for count, self.input_value in enumerate(self.names):
            self.count = count
            if count >= start_number:
                self.reserve_list()
                self.actions.click(search).perform()
                self.actions.send_keys(self.input_value).perform()
                self.actions.send_keys(Keys.ENTER)
                self.actions.perform()
                time.sleep(3)

                if self.check_availability():
                    continue
                if self.check_expiry_date(self.current_month()):
                    continue
                if self.check_expiry_date(self.next_month(1)):
                    continue


def run_with_retries():
    domain_checker = DomainChecker()
    try:
        domain_checker.get_start_page()
        time.sleep(20)
        domain_checker.main(get_from_reserve_list())
    except Exception as ex:
        print(EXCEPTION_MSG.format(ex))
        domain_checker.driver.quit()


if __name__ == "__main__":
    while True:
        run_with_retries()
