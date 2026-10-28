"""Ouvre la section Reels de Facebook avec un profil Firefox dédié."""

import json
import random
import time
from contextlib import suppress
from pathlib import Path

from colored import attr, fg
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

CONFIG_PATH = Path("config.json")
PROFILE_DIR = Path.home() / "selenium_profile"
HOME_URL = "https://www.facebook.com/"
REEL_URLS = ("https://www.facebook.com/reel/", "https://www.facebook.com/reels/")

COOKIE_XPATH = (
    "//button[contains(., 'Autoriser') or contains(., 'Accepter') "
    "or contains(., 'Allow') or contains(., 'Accept')]"
)
TRUST_XPATH = (
    "//*[(@role='button' or self::button) and ("
    "contains(., 'Faire confiance à cet appareil') or "
    "contains(., 'Faire confiance à ce navigateur') or "
    "contains(., 'Enregistrer le navigateur') or "
    "contains(., 'Trust this device') or "
    "contains(., 'Trust this browser') or "
    "contains(., 'Save browser'))]"
)
EMAIL_SELECTOR = "input[name='email'], input#email, input[type='email']"
PASSWORD_SELECTOR = "input[name='pass'], input#pass, input[type='password']"  # noqa: S105
BLOCKED_WORDS = ("login", "checkpoint", "two_step", "two_factor", "recover")


def log(message: str, color: str = "yellow_1") -> None:
    print(f"{fg(color)}{message}{attr('reset')}")


def pause(low: float = 0.8, high: float = 1.2) -> None:
    time.sleep(random.uniform(low, high))


def human_type(element: WebElement, text: str) -> None:
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.06, 0.25))
        if random.random() < 0.08:
            time.sleep(random.uniform(0.3, 0.8))


def human_click(driver: WebDriver, element: WebElement) -> None:
    width = int(element.size["width"] * 0.25)
    height = int(element.size["height"] * 0.25)
    (
        ActionChains(driver)
        .move_to_element_with_offset(
            element,
            random.randint(-width, width),
            random.randint(-height, height),
        )
        .pause(random.uniform(0.2, 0.6))
        .click()
        .perform()
    )


def random_scroll(driver: WebDriver) -> None:
    delta = random.randint(50, 200)
    driver.execute_script(f"window.scrollBy(0, {delta});")
    pause(0.3, 0.8)
    driver.execute_script(f"window.scrollBy(0, {-delta});")


def is_blocked(driver: WebDriver) -> bool:
    url = driver.current_url.lower()
    return any(word in url for word in BLOCKED_WORDS)


def wait_until_logged(driver: WebDriver, timeout: int = 180) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not is_blocked(driver):
            return True
        time.sleep(2)
    return False


def create_driver() -> WebDriver:
    options = Options()
    options.set_preference("intl.accept_languages", "fr-FR, fr")
    options.add_argument("-profile")
    options.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(random.randint(1200, 1400), random.randint(750, 900))
    return driver


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


def login(driver: WebDriver, email_box: WebElement, user: str, password: str) -> None:
    wait = WebDriverWait(driver, 20)

    human_click(driver, email_box)
    pause(0.4, 1.0)
    human_type(email_box, user)
    log("Email entered")
    pause(0.6, 1.5)

    password_box = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, PASSWORD_SELECTOR))
    )
    human_click(driver, password_box)
    pause(0.4, 1.0)
    human_type(password_box, password)
    log("Password entered")
    pause(0.8, 1.8)

    password_box.send_keys(Keys.RETURN)
    pause(4, 7)

    log("Check 2FA")
    click_trust_button(driver)

    if not wait_until_logged(driver):
        log(f"Toujours bloqué : {driver.current_url}", "red_1")


def open_reels(driver: WebDriver) -> bool:
    for url in REEL_URLS:
        driver.get(url)
        pause(4, 6)
        log(f"{url} -> {driver.current_url}")
        if "/reel" in driver.current_url and not is_blocked(driver):
            return True

    driver.get(HOME_URL)
    pause(3, 5)
    try:
        link = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/reel']"))
        )
    except TimeoutException:
        return False
    human_click(driver, link)
    pause(4, 6)
    log(f"Via menu -> {driver.current_url}")
    return "/reel" in driver.current_url


def main() -> None:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    driver: WebDriver | None = None
    try:
        driver = create_driver()
        driver.get(HOME_URL)
        log("Facebook Opened!")
        pause(2, 4)
        random_scroll(driver)
        accept_cookies(driver)

        email_box = find_login_form(driver)
        if email_box is None:
            log("Logged")
        else:
            login(driver, email_box, config["email"], config["password"])

        pause(2, 3)
        opened = open_reels(driver)
        driver.save_screenshot("reels.png")
        status = "ouverts" if opened else "NON ouverts"
        log(f"Reels {status} : {driver.current_url}", "green_1" if opened else "red_1")

        input(f"{fg('green_1')}Press anything to quit{attr('reset')}")
    except WebDriverException as exc:
        log(f"Failed to execute script: {exc}", "red_1")
        if driver is not None:
            driver.save_screenshot("error.png")
    finally:
        if driver is not None:
            driver.quit()
            log("Finished", "green_1")


if __name__ == "__main__":
    main()
