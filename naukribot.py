from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import logging
import pickle
import os


class NaukriBot:
    def __init__(self, delay=5):
        self.data = []
        self.email = 'pwgaikwad611@gmail.com'
        self.password = 'qqF*P9vfn/Nvv/J'
        if not os.path.exists("data"):
            os.makedirs("data")
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        self.delay = delay
        logging.info("Starting driver")
        self.driver = webdriver.Firefox(executable_path="geckodriver.exe")

    def login(self, email, password):
        """Go to naukri and login"""
        # go to naukri:
        logging.info("Logging in")
        self.driver.maximize_window()
        self.driver.get('https://www.naukri.com/nlogin/login')
        time.sleep(self.delay)

        self.driver.find_element_by_id('usernameField').send_keys(email)
        self.driver.find_element_by_id('passwordField').send_keys(password)

        self.driver.find_element_by_id('passwordField').send_keys(Keys.RETURN)
        time.sleep(self.delay)

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def search_naukri(self, keywords, location):
        """Enter keywords into search bar
        """
        logging.info("Searching jobs page")
        self.driver.get("https://www.naukri.com/browse-jobs/")
        # search based on keywords and location and hit enter
        self.wait_for_element_ready(By.CLASS_NAME, 'sugInp')
        time.sleep(self.delay)
        search_bars = self.driver.find_elements_by_class_name('sugInp')
        search_keywords = search_bars[0]
        search_keywords.send_keys(keywords)

        search_keywords.send_keys(Keys.TAB)
        search_bars = self.driver.find_elements_by_class_name('sugInp')
        search_location = search_bars[1]
        search_location.send_keys(location)
        search_location.send_keys(Keys.RETURN)
        time.sleep(self.delay)
        logging.info("Keyword search successful")
        time.sleep(self.delay)

    def wait(self, t_delay=None):
        """Just easier to build this in here.
        Parameters
        ----------
        t_delay [optional] : int
            seconds to WebDriverWait(self.driver, 20).
        """
        delay = self.delay if t_delay == None else t_delay
        time.sleep(delay)

    def scroll_to(self, job_list_item):
        """Just a function that will scroll to the list item in the column 
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", job_list_item)
        job_list_item.click()
        time.sleep(self.delay)

    def get_position_data(self, n):

        self.driver.get(self.driver.current_url)
        count = n  # Update the Number of Vacancy count you want to scrape.

        # This the the index variable of the elements from which data will be Scraped
        index, new_index, i = '0', 1, 0
        # Xpaths of the various element from which data will be scraped.
        heading_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])[' + \
            index+']/div/div/a'
        link_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])[' + \
            index+']/div/div/a'
        subheading_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])[' + \
            index+']/div/div/div/a'
        experience_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])[' + \
            index+']/div/div/ul/li[1]/span'
        salary_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])[' + \
            index+']/div/div/ul/li[2]/span'

        while i < count:

            for j in range(20):
                # Here we're replacing the Old index count of Xpath with New Index count.
                # Zfill(2) is used to put zeros to the left of any digit till 2 decimal places.
                temp_index = str(new_index).zfill(2)
                heading_xpath = heading_xpath.replace(index, temp_index)
                link_xpath = link_xpath.replace(index, temp_index)
                subheading_xpath = subheading_xpath.replace(index, temp_index)
                experience_xpath = experience_xpath.replace(index, temp_index)
                salary_xpath = salary_xpath.replace(index, temp_index)
                index = str(new_index).zfill(2)
                try:
                    # Capturing the Heading from webpage and storing that into Heading variable.
                    heading = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                        (By.XPATH, heading_xpath))).text
                    print(heading)
                except:
                    heading = "NULL"
                try:
                    link = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                        (By.XPATH, link_xpath))).get_attribute('href')
                    print(link)
                except:
                    link = "NULL"
                try:
                    subheading = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                        (By.XPATH, subheading_xpath))).text
                    print(subheading)
                except:
                    subheading = "NULL"
                try:
                    experience = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                        (By.XPATH, experience_xpath))).text
                    print(experience)
                except:
                    experience = "NULL"
                try:
                    salary = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                        (By.XPATH, salary_xpath))).text
                    print(salary)
                except:
                    salary = "Not Disclosed"

                self.data.append({
                    'position': heading,
                    'company': subheading,
                    'experience': experience,
                    'link': link,
                    'salary': salary
                })
                new_index += 1
                i += 1
                print("--------------------------- "+str(i) +
                      " ----------------------------------")

                if i >= count:
                    break
            if i >= count:
                break

            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[text() = "Next"]'))).click()
            new_index = 1
        return [heading, subheading, experience, salary]

    def wait_for_element_ready(self, by, text):
        try:
            WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((by, text)))
        except TimeoutException:
            logging.debug("wait_for_element_ready TimeoutException")
            pass

    def close_session(self):
        """This function closes the actual session"""
        logging.info("Closing session")
        self.driver.close()

    def run(self,  keywords, location, n):
        if os.path.exists("data/naukri_cookies.txt"):
            self.driver.get("https://www.naukri.com/")
            self.load_cookie("data/naukri_cookies.txt")
            self.driver.get("https://www.naukri.com/")
        else:
            self.login(
                email=self.email,
                password=self.password
            )
            self.save_cookie("data/naukri_cookies.txt")

        logging.info("Begin naukri keyword search")
        self.search_naukri(keywords, location)
        self.wait()

        self.get_position_data(n)

        logging.info("Done scraping.")
        logging.info("Closing DB connection.")
        self.close_session()
        return self.data


# if __name__ == "__main__":
#     email = 'pwgaikwad611@gmail.com'
#     password = "qqF*P9vfn/Nvv/J"
#     bot = NaukriBot()
#     bot.run(email, password, "Data Scientist", "Banglore")
