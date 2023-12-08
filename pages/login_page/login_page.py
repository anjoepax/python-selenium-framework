import logging

from selenium.webdriver.common.by import By
from base.base_page import BasePage
import utilities.custom_logger as cl


class LoginPage(BasePage):

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locator
    _username_field = "username"
    _password_field = "password"
    _login_btn = "login"
    _login_hello_msg = "//div[@class='woocommerce-MyAccount-content']/p[1]"
    _login_error_msg = "//ul[@class='woocommerce-error' and @role='alert']"

    def enter_username(self, username):
        self.wait_for_element(self._username_field, By.ID)
        self.clear_input_field(self._username_field, By.ID)
        self.enter_input_field(username, self._username_field, By.ID)

    def enter_password(self, password):
        self.wait_for_element(self._password_field, By.ID)
        self.clear_input_field(self._password_field, By.ID)
        self.enter_input_field(password, self._password_field, By.ID)

    def click_login_button(self):
        self.wait_for_element(self._login_btn, By.NAME)
        self.element_click(self._login_btn, By.NAME)

    def login(self, user_name="", password=""):
        self.enter_username(user_name)
        self.enter_password(password)
        self.click_login_button()

    def get_login_hello_msg_display(self):
        self.wait_for_element(self._login_hello_msg, By.XPATH)
        return self.get_element(self._login_hello_msg, By.XPATH).text

    def get_login_error_msg_display(self):
        self.wait_for_element(self._login_error_msg, By.XPATH)
        return self.get_element(self._login_error_msg, By.XPATH).text

    def verify_login_successful(self):
        result = self.is_element_present(self._login_hello_msg, By.XPATH)
        return result

    def verify_login_unsuccessful(self):
        result = self.is_element_present(self._login_error_msg, By.XPATH)
        return result
