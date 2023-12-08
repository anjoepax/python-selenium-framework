import unittest

import pytest
from assertpy import assert_that
from pages.login_page.login_page import LoginPage


@pytest.mark.usefixtures("setup")
class LoginTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.login_page = LoginPage(self.driver)

    def test_valid_login(self):
        self.login_page.login("ajblues", "Test123")
        is_login_success = self.login_page.verify_login_successful()
        assert_that(is_login_success).is_true()

    def test_invalid_login(self):
        self.login_page.login("AJTESTER", "Test123")
        is_login_unsuccessful = self.login_page.verify_login_unsuccessful()
        assert_that(is_login_unsuccessful).is_true()

    def test_login_without_username_password(self):
        self.login_page.login()
        is_login_unsuccessful = self.login_page.verify_login_unsuccessful()
        assert_that(is_login_unsuccessful).is_true()

    def test_login_with_password_and_without_username(self):
        self.login_page.login(password="Test123")
        is_login_unsuccessful = self.login_page.verify_login_unsuccessful()
        assert_that(is_login_unsuccessful).is_true()

