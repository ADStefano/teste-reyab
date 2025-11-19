from pathlib import Path
from selenium import webdriver

def chrome_driver_setup(download_folder: Path) -> webdriver.Chrome:
    """ Configura o webdriver Selenium """

    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("prefs", {
        "download.default_directory": str(download_folder),
        "safebrowsing.enabled": True,
        })
    
    return webdriver.Chrome(options=opts)