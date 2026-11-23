from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "test-results"

APPIUM_SERVER = "http://127.0.0.1:4723"
DEVICE_NAME = "emulator-5554"

APP_PATH = PROJECT_ROOT / "apps" / "mda.apk"
APP_PACKAGE = "com.saucelabs.mydemoapp.android"
APP_ACTIVITY = ".view.activities.SplashActivity"
APP_WAIT_ACTIVITY = "*.MainActivity"

DEFAULT_TIMEOUT = 10


@dataclass(frozen=True)
class Target:
    name: str
    device_name: str
    install_from_apk: bool
    no_reset: bool = False
    full_reset: bool = False
    new_command_timeout: int = 120


TARGETS = {
    "local": Target(name="local", device_name=DEVICE_NAME, install_from_apk=False),
    "dev": Target(
        name="dev", device_name=DEVICE_NAME, install_from_apk=False, no_reset=True
    ),
    "ci": Target(
        name="ci",
        device_name=DEVICE_NAME,
        install_from_apk=True,
        new_command_timeout=300,
    ),
}
