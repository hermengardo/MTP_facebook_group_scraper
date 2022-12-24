from datetime import datetime
from time import sleep
from random import random

import utils

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager


class Scraper:
    def __init__(self,
                 email: str,
                 password: str,
                 group_id: str,
                 pages: int,
                 implicitly_wait: int = 5,
                 explicitly_wait: int = 2,
                 headless=True) -> None:

        URL = "https://m.facebook.com/"
        OPTIONS = Options()
        OPTIONS.add_argument("--headless")
        PROFILE = webdriver.FirefoxProfile()
        PROFILE.set_preference("dom.webnotifications.enabled", False)
        PROFILE.set_preference("app.update.enabled", False)
        PROFILE.update_preferences()

        self.email = email
        self.password = password
        self.group_url = URL + "groups/" + group_id
        self.pages = pages
        self.explicitly_wait = explicitly_wait
        self.errors = 0
        self.driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            firefox_profile=PROFILE,
            options=OPTIONS if headless else None
        )

        # Clean log file
        utils.clean_log()

        # Open and set browser
        self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        with self.driver as driver:
            # Get page
            driver.get(URL)
            # Login
            self._login()
            # Retrieve data
            utils.save_as_csv(self._retrieve_posts())
            # Print total number of errors
            print("Finished.")
            if self.errors > 0:
                print(f"""Total number of failures: {self.errors}. Check log file.""")

    # Check if the login was successfull
    def _check_login(self):
        if self._popup_handler():
            return True
        else:
            try:
                WebDriverWait(self.driver, self.explicitly_wait).until(
                              EC.presence_of_element_located((
                                By.CSS_SELECTOR,
                                "#m_news_feed_stream"
                              )))
                return True
            except TimeoutException:
                return False

    def _get_group(self):
        # Go to group page
        self.driver.get(url=self.group_url)
        try:
            WebDriverWait(self.driver, self.explicitly_wait).until(
                          EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            r'#m_group_stories_container'
                          )))
        except TimeoutException:
            raise Exception("Unable to find the group.")

    def _login(self):
        print("Connecting...")
        # Login and verify
        account_box = WebDriverWait(self.driver,
                                    self.explicitly_wait).until(
                                    EC.presence_of_element_located((
                                        By.XPATH,
                                        r'//*[@id="m_login_email"]'
                                    )))
        password_box = self.driver.find_element(By.XPATH,
                                                r'//*[@id="m_login_password"]')
        press_btn = self.driver.find_element(By.XPATH,
                                             r'//*[@name="login"]')
        account_box.send_keys(self.email)
        password_box.send_keys(self.password)
        press_btn.click()

        # Check if login was successful
        if not self._check_login():
            raise Exception("Unsuccessful login.")
        else:
            print("Connected.")

    def _load_pages(self):
        for page in range(self.pages):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Loading {page + 1}º page")
            sleep(self.explicitly_wait + random())

    def _retrieve_posts(self):
        # Get group
        self._get_group()
        # Load pages
        self._load_pages()
        # Name, group_name, date, description, url, time
        data = []
        # Get links
        for url in self._retrieve_urls():
            # Delay between retrieves
            sleep(random())
            # Open a new tab
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            # Go to a post
            self.driver.get(url)
            potential_data = self._retrieve_data(url)
            if potential_data:
                data.append(potential_data)
                print(f"Total collected: {len(data)}")
            # Close the new tab
            self.driver.close()
            # return to original tab
            self.driver.switch_to.window(self.driver.window_handles[0])
        return data

    def _retrieve_data(self, url):
        # Name, date, groupname, description, url, time
        new_data = ["NAN", "NAN", "NAN", "NAN", url, datetime.now()]
        # Name, date, groupname, description
        paths = ['//*[@class="story_body_container"]/header/div/div[2]//div[1]/h3//strong[1]/a',
                 '//*[@class="story_body_container"]/header/div/div[2]/div/div/div/div[1]/div/a/abbr',
                 '//*[@class="story_body_container"]/header/div/div[2]//div[1]/h3/span/strong[2]/a',
                 '//*[@class="story_body_container"]/div']
        try:
            # Find elements and collect data
            for i in range(len(paths)):
                new_data[i] = self.driver.find_element(
                            By.XPATH,
                            paths[i]
                            ).text
            return new_data
        except NoSuchElementException as error:
            self.errors += 1
            # If data is empty, it doesn't save
            if new_data[0:4] == ["NAN", "NAN", "NAN", "NAN"]:
                print(f"Unable to find any element in: {url}")
                utils.log_error(error, self.errors, url)
                return False
            # Save errors in the log file 
            utils.log_error(error, self.errors, url)
            return new_data

    def _retrieve_urls(self):
        xpath = r'//*[@id="m_group_stories_container"]//section/article/div/div[1]/a'
        urls = WebDriverWait(self.driver, self.explicitly_wait).until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                xpath
            ))
        )
        cleaned_urls = []
        for url in urls:
            cleaned_urls.append(
                utils.parser_link(
                    url.get_attribute("href")
                    ))
        return cleaned_urls

    def _popup_handler(self):
        try:
            btn = WebDriverWait(self.driver, self.explicitly_wait).until(
                                EC.presence_of_element_located((
                                    By.CSS_SELECTOR,
                                    "a._54k8"
                                )))
            btn.click()
            return True
        except TimeoutException:
            return False
