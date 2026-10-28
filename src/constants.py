from pathlib import Path

CONFIG_PATH = Path("config.json")
PROFILE_DIR = Path.home() / "selenium_profile"
SCREENSHOT_DIR = Path("screenshots")

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
PASSWORD_SELECTOR = "input[name='pass'], input#pass, input[type='password']"  
REEL_LINK_SELECTOR = "a[href*='/reel']"

BLOCKED_WORDS = ("login", "checkpoint", "two_step", "two_factor", "recover")
