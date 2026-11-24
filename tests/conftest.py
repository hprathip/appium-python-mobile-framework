import re

import pytest
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from config import settings
from config.capabilities import build_options
from config.settings import TARGETS, Target


# ---------- choosing the packing list ----------

def pytest_addoption(parser):
    parser.addoption(
        "--target",
        action="store",
        default="local",
        choices=sorted(TARGETS),                 # typos like "cii" are rejected immediately
        help="Environment to run against",
    )


def pytest_report_header(config):
    return f"target: {config.getoption('--target')}"     # shows the target at the top of every run


@pytest.fixture(scope="session")
def target(request) -> Target:
    return TARGETS[request.config.getoption("--target")]


# ---------- the session (new rental car per test) ----------

@pytest.fixture
def driver(target):
    if target.install_from_apk and not settings.APP_PATH.exists():
        pytest.fail(f"APK not found at {settings.APP_PATH}")

    drv = webdriver.Remote(settings.APPIUM_SERVER, options=build_options(target))
    yield drv
    drv.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, settings.DEFAULT_TIMEOUT)


# ---------- the dashcam ----------

@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield                                        # pytest writes the report first
    if report.when == "call" and report.failed:          # the test body failed
        drv = item.funcargs.get("driver")                 # phone still connected (teardown hasn't run)
        if drv is not None:
            _save_evidence(drv, item.name)
    return report


def _save_evidence(drv, test_name: str) -> None:
    safe_name = re.sub(r"[^\w.-]", "_", test_name)        # safe folder name on Windows
    out_dir = settings.RESULTS_DIR / safe_name
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        drv.get_screenshot_as_file(str(out_dir / "screenshot.png"))
        (out_dir / "page_source.xml").write_text(drv.page_source, encoding="utf-8")
    except Exception as exc:                              # broken camera never hides the accident
        print(f"[evidence] could not save evidence for {test_name}: {exc}")