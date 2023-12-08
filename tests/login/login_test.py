import unittest

from assertpy import assert_that
from selenium import webdriver

from pages.login_page.login_page import LoginPage


class LoginTests(unittest.TestCase):

    def __initialize_app_and_browser_driver(self):
        base_url = "https://askomdch.com/account/"
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(base_url)
        return driver

    def test_valid_login(self):
        chrome_driver = self.__initialize_app_and_browser_driver()
        login_page = LoginPage(chrome_driver)
        login_page.login("ajblues", "Test123")
        is_login_success = login_page.verify_login_successful()
        assert_that(is_login_success).is_true()

    def test_invalid_login(self):
        chrome_driver = self.__initialize_app_and_browser_driver()
        login_page = LoginPage(chrome_driver)
        login_page.login("AJTESTER", "Test123")
        is_login_unsuccessful = login_page.verify_login_unsuccessful()
        assert_that(is_login_unsuccessful).is_true()

