from traceback import print_stack

from selenium.common import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import utilities.custom_logger as cl
import logging


class BasePage(object):

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def get_by_type(self, locator_type):
        """
        Custom method on getting the By type of element
        :param locator_type:
        :return:
        """
        locator_type = locator_type.lower()
        if locator_type == 'id':
            return By.ID
        elif locator_type == 'name':
            return By.NAME
        elif locator_type == 'xpath':
            return By.XPATH
        elif locator_type == 'css selector':
            return By.CSS_SELECTOR
        elif locator_type == 'class name':
            return By.CLASS_NAME
        elif locator_type == 'link text':
            return By.LINK_TEXT
        else:
            self.log.info(f"Locator type {locator_type} is not supported.")
        return False

    def get_element(self, locator, locator_type="id"):
        """
        Custom method for getting the element on the page
        :param locator:
        :param locator_type:
        :return:
        """
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info(f"Element found with locator [{locator}] and locator type [{locator_type}]")
        except:
            self.log.info(f"Element not found with locator [{locator}] and locator type [{locator_type}]")
            print_stack()
        return element

    def element_click(self, locator, locator_type="id"):
        """
        Custom method on clicking element on the page
        :param locator:
        :param locator_type:
        :return:
        """
        try:
            element = self.get_element(locator, locator_type)
            element.click()
            self.log.info(f"Clicked on element with locator [{locator}] and locator type [{locator_type}]")
        except:
            self.log.info(f"Cannot clicked on the element with locator [{locator}] and locator type [{locator_type}]")
            print_stack()

    def enter_input_field(self, data, locator, locator_type="id"):
        """
        Custom method to enter text on the field <input> tag
        :param data:
        :param locator:
        :param locator_type:
        :return:
        """
        try:
            element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info(f"Entered text on the element with locator [{locator}] and locator type [{locator_type}]")
        except:
            self.log.info(f"Cannot enter text on the element with locator [{locator}] and locator type [{locator_type}]")
            print_stack()

    def is_element_present(self, locator, by_type):
        """
        Custom method to check if a certain element is present on the page
        :param locator:
        :param by_type:
        :return:
        """
        try:
            element = self.driver.find_element(by_type, locator)
            if element is not None:
                self.log.info(f"Element locator [{locator}] is present in the page")
                return True
            else:
                self.log.info(f"Element locator [{locator}] is not present in the page")
                return False
        except:
            self.log.info(f"Element [{locator}] not found")
            print_stack()
            return False

    def is_element_presence_check(self, locator, by_type):
        """
        Custom method to check if list of elements is present on the page
        :param locator:
        :param by_type:
        :return:
        """
        try:
            element_list = self.driver.find_elements(by_type, locator)
            if len(element_list) > 0:
                self.log.info(f"Elements locator [{locator}] is present in the page")
                return True
            else:
                self.log.info(f"Elements locator [{locator}] is not present in the page")
                return False
        except:
            self.log.info(f"Elements [{locator}] not found")
            print_stack()
            return False

    def wait_for_element(self, locator, locator_type="id", time_out=10, poll_frequency=0.5):
        """
        Custom wait method
        :param locator:
        :param locator_type:
        :param time_out:
        :param poll_frequency:
        :return:
        """
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum :: " + str(time_out) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, 10, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(ec.element_to_be_clickable((by_type, locator)))
            self.log.info(f"Element appeared on the web page with locator [{locator}] and locator type [{locator_type}]")
        except:
            self.log.info(f"Element not appeared on the web page with locator [{locator}] and locator type [{locator_type}]")
            print_stack()
        return element
