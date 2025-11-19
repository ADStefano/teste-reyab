import tempfile
from pathlib import Path

from web_automation.web_automation import WebAutomation
from web_automation.config import load_config
from web_automation.web_driver import chrome_driver_setup

def web_automation_factory() -> WebAutomation:
    """ Factory para criar instâncias de WebAutomation """

    download_folder = Path(tempfile.mkdtemp(prefix="rpa_challange"))
    config = load_config()
    driver = chrome_driver_setup(download_folder=download_folder)
    return WebAutomation(config_parser=config, driver=driver, download_folder=download_folder)