import logging

from selenium.webdriver.common.by import By
from base.base_page import BasePage
import utilities.custom_logger as cl


class LoginPage(BasePage):
    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    _login_btn = ["LOGIN BUTTON", "login", By.NAME]
    _username_field = ["USERNAME FIELD", "username", By.ID]
    _password_field = ["PASSWORD FIELD", "password", By.ID]
    _login_hello_msg = ["LOGIN HELLO MESSAGE", "//div[@class='woocommerce-MyAccount-content']/p[1]", By.XPATH]
    _login_error_msg = ["LOGIN ERROR MESSAGE", "//ul[@class='woocommerce-error' and @role='alert']", By.XPATH]

    def enter_username(self, username):
        self.wait_for_element(self._username_field)
        self.clear_input_field(self.get_element(self._username_field))
        self.enter_input_field(username, self.get_element(self._username_field))

    def enter_password(self, password):
        self.wait_for_element(self._password_field)
        self.clear_input_field(self.get_element(self._password_field))
        self.enter_input_field(password, self.get_element(self._password_field))

    def click_login_button(self):
        self.wait_for_element(self._login_btn)
        self.element_click(self.get_element(self._login_btn))

    def login(self, user_name="", password=""):
        self.enter_username(user_name)
        self.enter_password(password)
        self.click_login_button()

    def get_login_hello_msg_display(self):
        self.wait_for_element(self._login_hello_msg)
        return self.get_element(self._login_hello_msg)[0].text

    def get_login_error_msg_display(self):
        self.wait_for_element(self._login_error_msg)
        return self.get_element(self._login_error_msg)[0].text

    def verify_login_successful(self):
        result = self.is_element_present(self.get_element(self._login_hello_msg))
        return result

    def verify_login_unsuccessful(self):
        result = self.is_element_present(self.get_element(self._login_error_msg))
        return result
