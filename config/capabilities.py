from appium.options.android import UiAutomator2Options

from config import settings
from config.settings import Target


def build_options(target: Target) -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.device_name = target.device_name
    options.app_wait_activity = settings.APP_WAIT_ACTIVITY
    options.no_reset = target.no_reset
    options.full_reset = target.full_reset
    options.new_command_timeout = target.new_command_timeout

    if target.install_from_apk:
        options.app = str(settings.APP_PATH)                 # "here's the file, install it"
    else:
        options.app_package = settings.APP_PACKAGE           # "it's already there, open it"
        options.app_activity = settings.APP_ACTIVITY

    return options