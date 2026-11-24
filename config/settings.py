from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "test-results"          # where failure evidence goes

APPIUM_SERVER = "http://127.0.0.1:4723"

APP_PATH = PROJECT_ROOT / "apps" / "mda.apk"
APP_PACKAGE = "com.saucelabs.mydemoapp.android"
APP_ACTIVITY = ".view.activities.SplashActivity"
APP_WAIT_ACTIVITY = "*.MainActivity"

DEFAULT_TIMEOUT = 10


@dataclass(frozen=True)                                # laminated: tests can read, not change
class Target:
    name: str
    device_name: str
    install_from_apk: bool                             # True = install the APK, False = already on the phone
    no_reset: bool = False                             # True = keep app data between sessions
    full_reset: bool = False                           # True = uninstall + reinstall every session
    new_command_timeout: int = 120                     # the waiter: seconds of silence before the session is closed


TARGETS = {                                            # one packing list per trip
    "local": Target(name="local", device_name="emulator-5554", install_from_apk=False),
    "dev":   Target(name="dev",   device_name="emulator-5554", install_from_apk=False, no_reset=True),
    "ci":    Target(name="ci",    device_name="emulator-5554", install_from_apk=True, new_command_timeout=300),
}