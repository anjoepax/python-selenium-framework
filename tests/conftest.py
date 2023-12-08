import logging

import allure
import pytest
from allure_commons.types import AttachmentType
from base.webdriver_factory import WebDriverFactory
import utilities.custom_logger as cl
from string import ascii_letters, digits
from random import choice

log = cl.custom_logger(logging.DEBUG)


@pytest.fixture(autouse=True)
def setup(request, browser, base_url, run_mode):
    driver_factory = WebDriverFactory(browser, run_mode)
    driver = driver_factory.get_webdriver_instance()
    driver.get(base_url)
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()


"""
Can be use to run for a one time setup
"""


# @pytest.fixture(scope="class")
# def one_time_setup(request, browser, os_type):
#     print("One time browser driver setup")
#     driver_factory = WebDriverFactory(browser)
#     driver = driver_factory.get_webdriver_instance()
#     if request.cls is not None:
#         request.cls.driver = driver
#     yield driver
#     print("One time module teardown")
#     driver.quit()
#     print()


def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--os_type", help="Type of operating system")
    parser.addoption("--base_url", help="Environment url")
    parser.addoption("--run_mode", help="Select local or remote")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def os_type(request):
    return request.config.getoption("--os_type")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture(scope="session")
def run_mode(request):
    return request.config.getoption("--run_mode")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    screenshot_name = ''.join([choice(ascii_letters + digits) for i in range(16)])
    if result.failed:
        allure.attach(
            item.cls.driver.get_screenshot_as_png(),
            screenshot_name,
            attachment_type=AttachmentType.PNG
        )


@pytest.fixture(scope="function", autouse=True)
def test_start_log(request):
    log.info(f"************************* STARTED TEST [{request.node.name}] *************************")

    def fin():
        log.info(f"************************* COMPLETED TEST [{request.node.name}] *************************")

    request.addfinalizer(fin)
