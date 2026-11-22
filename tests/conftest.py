import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

from config import settings

@pytest.fixture
def driver():
    if not settings.APP_PATH.exists():
        pytest.fail(f"APK not found at {settings.APP_PATH}")

    options = UiAutomator2Options()
    options.device_name = settings.DEVICE_NAME
    options.app = str(settings.APP_PATH)
    options.app_wait_activity = settings.APP_WAIT_ACTIVITY

    drv = webdriver.Remote(settings.APPIUM_SERVER, options=options)

    yield drv
    drv.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, settings.DEFAULT_TIMEOUT)