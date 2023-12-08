import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import utilities.custom_logger as cl


class WebDriverFactory:

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, browser, run_mode="local", remote_grid_url="http://localhost:4444/wd/hub"):
        self.browser = browser
        self.run_mode = run_mode
        self.remote_grid_url = remote_grid_url

    def get_webdriver_instance(self):
        if self.run_mode.lower() == "remote":
            options = Options()
            if self.browser.lower() == "chrome":
                options.set_capability("browserName", "chrome")
            elif self.browser.lower() == "firefox":
                options.set_capability("browserName", "firefox")
            else:
                options.set_capability("browserName", "MicrosoftEdge")
            driver = webdriver.Remote(command_executor=self.remote_grid_url, options=options)
        else:
            if self.browser.lower() == "chrome":
                self.log.info("RUNNING ON CHROME BROWSER")
                driver = webdriver.Chrome()
            elif self.browser.lower() == "firefox":
                self.log.info("RUNNING ON FIREFOX BROWSER")
                driver = webdriver.Firefox()
            else:
                self.log.info("RUNNING ON EDGE BROWSER")
                driver = webdriver.Edge()
            driver.maximize_window()
        return driver

