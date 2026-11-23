import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

CATALOG_TITLE = (AppiumBy.ACCESSIBILITY_ID, "title")

@pytest.mark.smoke
def test_app_launches_to_catalog(wait):
    title = wait.until(EC.visibility_of_element_located(CATALOG_TITLE))
    assert title.text == "Products"