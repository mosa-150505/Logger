import random
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


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
