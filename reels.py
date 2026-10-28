from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.browser import is_blocked
from src.constants import HOME_URL, REEL_LINK_SELECTOR, REEL_URLS
from src.human import human_click, pause
from src.logger import log


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
            ec.element_to_be_clickable((By.CSS_SELECTOR, REEL_LINK_SELECTOR))
        )
    except TimeoutException:
        return False
    human_click(driver, link)
    pause(4, 6)
    log(f"Via menu -> {driver.current_url}")
    return "/reel" in driver.current_url
