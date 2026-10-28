from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from src.auth import ensure_logged_in
from src.browser import create_driver, open_facebook, save_screenshot
from src.config import ConfigError, load_config
from src.human import pause
from src.logger import colorize, log
from src.reels import open_reels


def main() -> None:
    try:
        config = load_config()
    except ConfigError as exc:
        log(str(exc), "red_1")
        return

    driver: WebDriver | None = None
    try:
        driver = create_driver()
        open_facebook(driver)
        ensure_logged_in(driver, config)

        pause(2, 3)
        opened = open_reels(driver)
        save_screenshot(driver, "reels.png")
        status = "opened" if opened else "closed"
        log(f"Reels {status} : {driver.current_url}", "green_1" if opened else "red_1")

        input(colorize("Press anything to quit", "green_1"))
    except WebDriverException as exc:
        log(f"Failed to execute script: {exc}", "red_1")
        if driver is not None:
            save_screenshot(driver, "error.png")
    finally:
        if driver is not None:
            driver.quit()
            log("Finished", "green_1")


if __name__ == "__main__":
    main()
