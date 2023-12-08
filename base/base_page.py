import logging
from traceback import print_stack

from selenium.common import (NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import utilities.custom_logger as cl


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

    def get_element(self, element_params):
        """
        :param element_params:
        :return:
        """
        element = None
        try:
            locator_type = element_params[2].lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, element_params[1])
            self.log.info(
                f"Element [{element_params[0]}] found with locator [{element_params[1]}] and locator type [{element_params[2]}]")
        except:
            self.log.info(
                f"Element [{element_params[0]}] not found with locator [{element_params[1]}] and locator type [{element_params[2]}]")
            print_stack()
        return element, element_params[0]

    def element_click(self, get_element):
        """
        :param get_element:
        :return:
        """
        element_name = get_element[1]
        try:
            element = get_element[0]
            element.click()
            self.log.info(f"[{element_name}] element is clicked")
        except:
            self.log.info(f"Cannot clicked on the [{element_name}] element")
            print_stack()

    def enter_input_field(self, data, get_element: list):
        """
        :param data:
        :param get_element:
        :return:
        """
        element_name = get_element[1]
        try:
            element = get_element[0]
            element.send_keys(data)
            self.log.info(f"Entered text on the [{element_name}] element")
        except:
            self.log.info(
                f"Cannot enter text on the [{element_name}] element")
            print_stack()

    def clear_input_field(self, get_element: list):
        """
        :param get_element:
        :return:
        """
        element_name = get_element[1]
        try:
            element = get_element[0]
            element.clear()
            self.log.info(f"Input field [{element_name}] is cleared")
        except:
            self.log.info(f"Cannot clear [{element_name}] field")
            print_stack()

    def is_element_present(self, get_element):
        """
        :param get_element:
        :return:
        """
        element_name = get_element[1]
        try:
            element = get_element[0]
            if element is not None:
                self.log.info(f"Element [{element_name}] is present in the page")
                return True
            else:
                self.log.info(f"Element [{element_name}] is not present in the page")
                return False
        except:
            self.log.info(f"Element [{element_name}] not found")
            print_stack()
            return False

    # def is_element_presence_check(self, get_element: list):
    #     """
    #     :param get_element:
    #     :return:
    #     """
    #     element_name = get_element[1]
    #     try:
    #         element_list = self.driver.find_elements(by_type, locator)
    #         if len(element_list) > 0:
    #             self.log.info(f"Elements locator [{locator}] is present in the page")
    #             return True
    #         else:
    #             self.log.info(f"Elements locator [{locator}] is not present in the page")
    #             return False
    #     except:
    #         self.log.info(f"Elements [{locator}] not found")
    #         print_stack()
    #         return False

    def wait_for_element(self, element_params: list, time_out=10, poll_frequency=0.5):
        """
        :param element_params:
        :param time_out:
        :param poll_frequency:
        :return:
        """
        element = None
        try:
            by_type = self.get_by_type(element_params[2])
            self.log.info("Waiting for maximum :: " + str(time_out) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, 10, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(ec.element_to_be_clickable((by_type, element_params[1])))
            self.log.info(
                f"Element [{element_params[0]}] appeared on the web page with locator [{element_params[1]}] and locator type [{element_params[2]}]")
        except:
            self.log.info(
                f"Element [{element_params[0]}] not appeared on the web page with locator [{element_params[1]}] and locator type [{element_params[2]}]")
            print_stack()
        return element
