from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

APPIUM_SERVER = "http://127.0.0.1:4723"
DEVICE_NAME = "emulator-5554"

APP_PATH = PROJECT_ROOT/"apps"/"mda.apk"
APP_PACKAGE = "com.saucelabs.mydemoapp.android"
APP_ACTIVITY = ".view.activities.SplashActivity"
APP_WAIT_ACTIVITY = "*.MainActivity"

DEFAULT_TIMEOUT = 10

