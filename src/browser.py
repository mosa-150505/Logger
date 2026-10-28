import random

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from src.constants import BLOCKED_WORDS, HOME_URL, PROFILE_DIR, SCREENSHOT_DIR
from src.human import pause, random_scroll
from src.logger import log


def create_driver() -> WebDriver:
    options = Options()
    options.set_preference("intl.accept_languages", "fr-FR, fr")
    options.add_argument("-profile")
    options.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(random.randint(1200, 1400), random.randint(750, 900))
    return driver


def open_facebook(driver: WebDriver) -> None:
    driver.get(HOME_URL)
    log("Facebook Opened!")
    pause(2, 4)
    random_scroll(driver)


def is_blocked(driver: WebDriver) -> bool:
    url = driver.current_url.lower()
    return any(word in url for word in BLOCKED_WORDS)


def save_screenshot(driver: WebDriver, name: str) -> None:
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    driver.save_screenshot(str(SCREENSHOT_DIR / name))
