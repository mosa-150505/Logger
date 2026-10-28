import time
from contextlib import suppress

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.browser import is_blocked
from src.config import Config
from src.constants import (
    COOKIE_XPATH,
    EMAIL_SELECTOR,
    PASSWORD_SELECTOR,
    TRUST_XPATH,
)
from src.human import human_click, human_type, pause
from src.logger import log


def wait_until_logged(driver: WebDriver, timeout: int = 180) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not is_blocked(driver):
            return True
        time.sleep(2)
    return False


def accept_cookies(driver: WebDriver) -> None:
    with suppress(TimeoutException):
        button = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.XPATH, COOKIE_XPATH))
        )
        human_click(driver, button)
        pause()


def find_login_form(driver: WebDriver) -> WebElement | None:
    try:
        return WebDriverWait(driver, 4).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, EMAIL_SELECTOR))
        )
    except TimeoutException:
        return None


def click_trust_button(driver: WebDriver) -> None:
    try:
        button = WebDriverWait(driver, 120).until(
            ec.element_to_be_clickable((By.XPATH, TRUST_XPATH))
        )
    except TimeoutException:
        log("Cannot find trust button")
        return
    pause(1, 2)
    human_click(driver, button)
    log("Trusted", "green_1")
    pause(3, 5)


def login(driver: WebDriver, email_box: WebElement, config: Config) -> None:
    wait = WebDriverWait(driver, 20)

    human_click(driver, email_box)
    pause(0.4, 1.0)
    human_type(email_box, config.email)
    log("Email entered")
    pause(0.6, 1.5)

    password_box = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, PASSWORD_SELECTOR))
    )
    human_click(driver, password_box)
    pause(0.4, 1.0)
    human_type(password_box, config.password)
    log("Password entered")
    pause(0.8, 1.8)

    password_box.send_keys(Keys.RETURN)
    pause(4, 7)

    log("Check 2FA")
    click_trust_button(driver)

    if not wait_until_logged(driver):
        log(f"Blocked : {driver.current_url}", "red_1")


def ensure_logged_in(driver: WebDriver, config: Config) -> None:
    accept_cookies(driver)
    email_box = find_login_form(driver)
    if email_box is None:
        log("Logged")
        return
    login(driver, email_box, config)
